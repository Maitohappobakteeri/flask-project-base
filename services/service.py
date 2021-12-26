from flask_jwt_extended import get_jwt_identity


def current_user_id():
    return get_jwt_identity()["user"]


def current_client_id():
    return get_jwt_identity()["client"]


class Service:
    def __init__(self, session):
        self._session = session
        self._query = self._session.query
