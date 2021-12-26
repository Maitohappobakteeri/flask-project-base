from services.example import ExampleService
from models.example import MyExampleSchema, NewExampleSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Example"],

    "operationId": "newExample",

    "summary": "Creates a new example",

    "requestBody": {
        "description": "the **new** example",
        "required": "true",
        "title": "newExampleDto",
        "content": {
            "application/json": {
                "schema": NewExampleSchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Created example",
            "content": {
                "application/json": {
                    "schema": MyExampleSchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('message', type=str)


class ExampleNewResource(Resource):
    decorators = [jwt_required]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(MyExampleSchema.marshaller())
    def post(self, session):
        args = _parser.parse_args()
        examples = ExampleService(session)
        return examples.new(args.message)
