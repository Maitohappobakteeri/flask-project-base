from services.auth import AuthService
from db import with_session

from flask import request
from flask_restful import Resource


class LoginResource(Resource):
    @with_session
    def post(self, session):
        authService = AuthService(session)
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        client = request.json.get('client', None)
        tokens = authService.login(username, password, client)
        if tokens:
            return tokens, 200
        return {"msg": "Unauthorized"}, 401
