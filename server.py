import os
import flask
import requests
import werkzeug.security
from flask import Flask, request, url_for, render_template, redirect, jsonify, \
    make_response
from flask_login import LoginManager, current_user, login_required, login_user, \
    logout_user
from werkzeug.security import generate_password_hash
from data import db_session, server_api, flask_forms
from data.users import User, get_user, get_user_by_login

db_session.global_init('db/project_data_base.db')

app = Flask(__name__)
app.register_blueprint(server_api.blueprint)
app.config.from_object('data.config')  # required to use flask_wtf

login_manager = LoginManager()
login_manager.init_app(app)

URL_SITE = 'http://127.0.0.1:5000'  # need for using own API


@login_manager.user_loader
def load_user(user_id):  # necessarily to be
    return get_user(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    url_index_css = url_for('static', filename='css/index.css')
    params = {'title': 'Титл', 'css_styles': [url_index_css], 'user': current_user}
    return render_template('index.html', **params)


@app.get('/register')
def get_register(message=None):
    url_register_css = url_for('static', filename='css/register.css')
    params = {'title': 'Регистрация', 'css_styles': [url_register_css], 'user': current_user,
              'form': flask_forms.Register_Form()}
    if not message is None:
        params['message'] = message
    return render_template('register.html', **params)


@app.post('/register')
def post_register():
    form = flask_forms.Register_Form()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return get_register(message='Пароли не совпадают')
        # sending request to api
        # key: register_key
        response = requests.post(URL_SITE + '/api/register', json={'login': form.login.data,
                                                                   'password': werkzeug.security.generate_password_hash(
                                                                       form.password.data)},
                                 params={'key': 'register_key'})
        try:
            json_response = response.json()
        except Exception:
            return get_register(message='Что-то пошло не так')
        if json_response['message'] == 'user already exists':
            return get_register(message='Пользователь с таким логином уже существует')
        if json_response['message'] == 'OK':
            user = get_user_by_login(form.login.data)
            login_user(user)
            return redirect('/')
    return get_register()


@app.get('/login')
def get_login(message=None):
    url_login_css = url_for('static', filename='css/login.css')
    params = {'title': 'Вход', 'css_styles': [url_login_css], 'user': current_user,
              'form': flask_forms.Login_Form()}
    if not message is None:
        params['message'] = message
    return render_template('login.html', **params)


@app.post('/login')
def post_login():
    form = flask_forms.Login_Form()
    if form.validate_on_submit():
        # sending request to api
        # key: login_key
        response = requests.post(URL_SITE + '/api/login',
                                 json={'login': form.login.data, 'password': form.password.data},
                                 params={'key': 'login_key'})
        try:
            json_response = response.json()
        except Exception:
            return get_login(message='Что-то пошло не так')
        if json_response['message'] in ['user doesnt exist', 'wrong password']:
            return get_login(message='Неверный логин или пароль')
        if json_response['message'] == 'OK':
            user = get_user_by_login(form.login.data)
            login_user(user)
            return redirect('/')
    return get_login()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
