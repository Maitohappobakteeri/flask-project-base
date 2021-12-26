import environment

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import alembic.config
from flask_restful import abort

from contextlib import contextmanager


_alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.main(argv=_alembicArgs)

Session = sessionmaker()
Engine = create_engine(environment.ConnectionString)
Session.configure(bind=Engine, autocommit=False)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        abort(500)
        session.rollback()
        raise
    finally:
        session.close()


def with_session(fun):
    def wrapped(self, *args, **kwargs):
        with session_scope() as session:
            return fun(self, session, *args, **kwargs)
    return wrapped


def with_session2(fun):
    def wrapped(*args, **kwargs):
        with session_scope() as session:
            return fun(session, *args, **kwargs)
    return wrapped
