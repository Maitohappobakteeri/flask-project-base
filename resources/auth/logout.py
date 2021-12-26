from services.auth import AuthService
from db import with_session

from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required
)


class LogoutResource(Resource):
    decorators = [jwt_required]

    @with_session
    def delete(self, session):
        auth = AuthService(session)
        auth.logout()
        return {"msg": "Successfully logged out"}
