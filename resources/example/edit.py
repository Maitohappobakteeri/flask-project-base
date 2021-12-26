from services.example import ExampleService
from models.example import MyExampleSchema
from db import with_session

from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Example"],

    "operationId": "editExample",

    "summary": "Edit example",

    "parameters": [
        {
            "in": "path",
            "name": "exampleId",
            "schema": {"type": "integer"},
            "required": "true",
            "description": "Example to be edited"
        },
    ],

    "responses": {
        "200": {
            "description": "Edited example",
            "content": {
                "application/json": {
                    "schema": MyExampleSchema.schemaSpecRef()
                }
            }
        }
    }
}


class ExampleEditResource(Resource):
    decorators = [jwt_required]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(MyExampleSchema.marshaller())
    def put(self, session, exampleId):
        examples = ExampleService(session)
        return examples.edit(exampleId)
