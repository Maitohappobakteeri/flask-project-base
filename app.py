#!flask/bin/python

import environment
from db import with_session2

from flask import Flask, jsonify
from flask_restful import abort, Api
from flask_jwt_extended import (
    JWTManager
)

from flasgger import Swagger
import flask_restful

import datetime

from services.auth import AuthService

from resources.user.user import UserResource

from resources.example.new import ExampleNewResource
from resources.example.edit import ExampleEditResource
from resources.example.history import ExampleHistoryResource

from resources.auth.login import LoginResource
from resources.auth.refresh import RefreshResource
from resources.auth.logout import LogoutResource

from models.schema import openapiSchemas

from collections import OrderedDict


def marshal(data, fields, envelope=None):
    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls

    if isinstance(data, (list, tuple)):
        return (OrderedDict([(envelope, [marshal(d, fields) for d in data])])
                if envelope else [marshal(d, fields) for d in data])

    items = ((k, marshal(data, v) if isinstance(v, dict)
              else make(v).output(k, data))
             for k, v in fields.items())
    # filtering None
    items = ((k, v) for k, v in items if v is not None)
    return OrderedDict([(envelope, OrderedDict(items))]) \
        if envelope \
        else OrderedDict(items)


flask_restful.marshal = marshal

app = Flask(__name__)
app.config['SECRET_KEY'] = environment.Secret
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config['SWAGGER'] = {"openapi": "3.0.3"}
app.config['PROPAGATE_EXCEPTIONS'] = True

swagger_config = {
    "headers": [],
    "servers": [
        {
            "url": "http://127.0.0.1:5000/",
            "description": "Local"
        }
    ],
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "title": environment.AppName,
    "version": '0.0.1',
    "termsOfService": "",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "description": "",
}

jwt = JWTManager(app)
swagger = Swagger(app, config=swagger_config, template={
    "components": {
        "schemas": openapiSchemas,
    },
    "definitions": openapiSchemas
    }
)

if environment.useCors:
    from flask_cors import CORS
    CORS(app)

api = Api(app, catch_all_404s=True)
api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
api.add_resource(RefreshResource, '/refresh')
api.add_resource(LogoutResource, '/logout')

api.add_resource(ExampleNewResource, '/example')
api.add_resource(ExampleEditResource, '/example/<exampleId>')
api.add_resource(ExampleHistoryResource, '/example')


@jwt.token_in_blacklist_loader
@with_session2
def check_if_token_not_in_use(session, decrypted_token):
    jti = decrypted_token['jti']
    authService = AuthService(session)
    usersTokens = authService.tokens(decrypted_token["identity"])
    return jti not in (token.jti for token in usersTokens)


@app.route('/version', methods=['GET'])
def version():
    return jsonify({"app": environment.AppName}), 200


@app.route('/')
def index():
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
