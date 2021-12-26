from .service import Service, current_user_id, current_client_id
from .user import UserService
from models.auth_token import AuthToken
import datetime
from datetime import datetime as dt
from werkzeug.security import check_password_hash
from utility import isTrue, isFalse, isNone, notNone
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token
)


class AuthService(Service):
    def __init__(self, session):
        super().__init__(session)
        self.userService = UserService(session)

    def login(self, username, password, client):
        self.remove_expired()
        userService = self.userService
        user = userService.userWithUsername(username)
        if user and check_password_hash(user.password, password):
            identity = {
                "user": user.id,
                "client": client
            }
            self.logout(identity)
            accessToken = create_access_token(identity=identity)
            refreshToken = create_refresh_token(identity=identity)

            self.add_token(accessToken)
            self.add_token(refreshToken)

            return {
                "accessToken": accessToken,
                "refreshToken": refreshToken
            }

        return None

    def refresh(self):
        self.remove_expired()
        current_user = current_user_id()
        client = current_client_id()
        identity = {
            "user": current_user,
            "client": client
        }
        accessToken = create_access_token(identity=identity)
        refreshToken = create_refresh_token(identity=identity)

        self.remove_current_refresh_token()
        self.add_token(accessToken)
        self.add_token(refreshToken)

        return {
            "accessToken": accessToken,
            "refreshToken": refreshToken
        }

    def add_token(self, token):
        decoded = decode_token(token)
        identity = decoded["identity"]
        token = AuthToken(
            jti=decoded["jti"],
            owner=identity["user"],
            access=(decoded["type"] == "access"),
            expires_at=dt.utcfromtimestamp(decoded["exp"]),
            client=identity["client"]
        )

        self._session.add(token)
        self._session.commit()
        return token

    def remove_expired(self):
        for token in self._query(AuthToken) \
                .filter(AuthToken.expires_at < datetime.datetime.utcnow()) \
                .all():
            self._session.delete(token)
        self._session.commit()

    def remove_current_refresh_token(self):
        for token in self._query(AuthToken) \
                   .filter(AuthToken.owner == current_user_id()) \
                   .filter(AuthToken.client == current_client_id()) \
                   .filter(isFalse(AuthToken.access)) \
                   .all():
            self._session.delete(token)
        self._session.commit()

    def tokens(self, identity=None):
        if identity is None:
            return self._query(AuthToken) \
                       .all()
        return self._query(AuthToken) \
                   .filter(AuthToken.owner == identity["user"]) \
                   .filter(AuthToken.client == identity["client"]) \
                   .all()

    def tokens_current_user(self):
        return self._query(AuthToken) \
                   .filter(AuthToken.owner == current_user_id()) \
                   .filter(AuthToken.client == current_client_id()) \
                   .filter(
                        AuthToken.expires_at >= datetime.datetime.utcnow()) \
                   .all()

    def tokens_for_user(self, identity):
        return self._query(AuthToken) \
                   .filter(AuthToken.owner == identity["user"]) \
                   .filter(AuthToken.client == identity["client"]) \
                   .filter(
                       AuthToken.expires_at >= datetime.datetime.utcnow()) \
                   .all()

    def logout(self, identity=None):
        if identity is None:
            for token in self.tokens_current_user():
                self._session.delete(token)
        else:
            for token in self.tokens_for_user(identity):
                self._session.delete(token)
        self._session.commit()
