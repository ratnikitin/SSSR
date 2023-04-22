import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    surname = sa.Column(sa.String, nullable=True)
    # about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sa.Column(sa.String,
                      index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime,
    #                                  default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        return self.hashed_password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

# мб реализация избранного
# class News(SqlAlchemyBase):
#     __tablename__ = 'news'
#
#     id = sa.Column(sa.Integer,
#                    primary_key=True, autoincrement=True)
#     title = sa.Column(sa.String, nullable=True)
#     author = sa.Column(sa.String, nullable=True)
#
#     user_id = sa.Column(sa.Integer,
#                         sa.ForeignKey("users.id"))
#     user = orm.relationship('User')
