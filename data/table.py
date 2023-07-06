import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Some_table(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'table'
    inf_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    some_information = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<Table id: {self.inf_id}>'