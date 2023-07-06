import flask

from flask import jsonify, request
from . import db_session
from .users import User
from . import security

blueprint = flask.Blueprint('server_api', __name__, template_folder='templates')


@blueprint.post('/api/register')
def register_api():
    if not security.check_key('register', request.args.get('key', '')):
        return jsonify({'message': 'access denied'})
    data = request.json
    session = db_session.create_session()
    if session.query(User).filter(User.login == data['login']).first():
        return jsonify({'message': 'user already exists'})
    user = User(login=data['login'])
    user.set_password(data['password'])
    session.add(user)
    session.commit()
    return jsonify({'message': 'OK'})


@blueprint.post('/api/login')
def login_api():
    if not security.check_key('login', request.args.get('key', '')):
        return jsonify({'message': 'access denied'})
    data = request.json
    session = db_session.create_session()
    user = session.query(User).filter(User.login == data['login']).first()
    if not user:
        return jsonify({'message': 'user doesnt exist'})
    if not user.check_password(data['password']):
        return jsonify({'message': 'wrong password'})
    return jsonify({'message': 'OK'})
