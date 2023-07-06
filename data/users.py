import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash
from .db_session import SqlAlchemyBase, create_session


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
    # user class example
    # SqlAlchemyBase for db, UserMixin for Flask-login, SerializerMixin for idk
    __tablename__ = 'users'
    # db columns
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    some_information = sqlalchemy.Column(sqlalchemy.String)

    def get_id(self):  # necessarily to be
        return self.user_id

    def set_password(self, password):
        self.hashed_password = password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User id: {self.user_id}; login: {self.login}>'


def get_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


def get_user_by_login(login):
    db_sess = create_session()
    return db_sess.query(User).filter(User.login == login).first()
