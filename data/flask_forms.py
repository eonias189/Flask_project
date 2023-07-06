from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    DateField, SelectField
from wtforms.validators import DataRequired


class Register_Form(FlaskForm):  # form for registration
    # validator DataRequired requires data in field
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться', validators=[])


class Login_Form(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
