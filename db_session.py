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
    email = sa.Column(sa.String,
                      index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        return self.hashed_password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Music(SqlAlchemyBase):
    __tablename__ = 'favs'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    sound_path = sa.Column(sa.String, nullable=True)
    picture_path = sa.Column(sa.String, nullable=True)
    author_name = sa.Column(sa.String, nullable=True)
    track_name = sa.Column(sa.String, nullable=True)
