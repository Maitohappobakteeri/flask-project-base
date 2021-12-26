from services.example import ExampleService
from models.example import MyExampleSchema
from db import with_session

from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Example"],

    "operationId": "loadHistory",

    "summary": "Gets example data",

    "parameters": [
        {
            "in": "query",
            "name": "start",
            "schema": {"type": "integer"},
            "required": "true",
            "description": "Page start"
        },
        {
            "in": "query",
            "name": "amount",
            "schema": {"type": "integer"},
            "required": "true",
            "description": "Max rows returned"
        }
    ],

    "responses": {
        "200": {
            "description": "History",
            "content": {
                "application/json": {
                    "schema": {
                      "type": "array",
                      "items": MyExampleSchema.schemaSpecRef()
                    }
                }
            }
        }
    }
}


class ExampleHistoryResource(Resource):
    decorators = [jwt_required]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(MyExampleSchema.marshaller())
    def get(self, session):
        args = request.args
        examples = ExampleService(session)
        return examples.history(args["start"], args["amount"])
