from flask_restful import fields

from enum import Enum

openapiSchemas = {}


class PropertyType(Enum):
    integer = "integer"
    string = "string"
    boolean = "boolean"
    date = "date"
    datetime = "datetime"
    object = "object"
    array = "array"
    # self = "self"


def propertyTypeToMarshallerField(property):
    type = property.type
    required = property.required

    if required:
        return {
            PropertyType.integer: fields.Integer(),
            PropertyType.string: fields.String(),
            PropertyType.boolean: fields.Boolean(),
            PropertyType.date: fields.DateTime(dt_format='rfc822'),
            PropertyType.datetime: fields.DateTime(dt_format='rfc822'),
        }[type]
    else:
        return {
            PropertyType.integer: fields.Integer(default=None),
            PropertyType.string: fields.String(default=None),
            PropertyType.boolean: fields.Boolean(default=None),
            PropertyType.date: fields.DateTime(
                dt_format='rfc822',
                default=None
            ),
            PropertyType.datetime: fields.DateTime(
                dt_format='rfc822',
                default=None
            ),
        }[type]


def propertyTypeToOpenapiSpec(type):
    return {
        PropertyType.integer: "integer",
        PropertyType.string: "string",
        PropertyType.boolean: "boolean",
        PropertyType.date: "string",
        PropertyType.datetime: "string",
    }[type]


class Property:
    def __init__(self, name, type, **kwargs):
        self.name = name
        self.type = type
        self.schema = kwargs.get("schema")

        self.required = kwargs.get("required")
        if self.required is None:
            self.required = True

        self.items = kwargs.get("items")


class Schema:
    def __init__(self, name, properties):
        self.name = name + "Dto"
        self.properties = properties
        openapiSchemas[self.name] = self.openapiSpec()[self.name]

    def marshaller(self):
        m = {}
        for p in self.properties:
            if p.type == PropertyType.array:
                m[p.name] = fields.List(fields.Nested(p.items.marshaller()))
            elif p.type == PropertyType.object:
                m[p.name] = fields.Nested(p.schema.marshaller())
            else:
                m[p.name] = propertyTypeToMarshallerField(p)
        return m

    def openapiSpec(self):
        obj = {}
        obj["type"] = "object"

        props = {}
        for p in self.properties:
            if p.type == PropertyType.array:
                props[p.name] = {
                    "type": "array",
                    "items": p.items.schemaSpecRef()
                }
            elif p.type == PropertyType.object:
                props[p.name] = p.schema.schemaSpecRef()
            else:
                props[p.name] = {
                    "type": propertyTypeToOpenapiSpec(p.type)
                }
        obj["properties"] = props

        required = []
        for p in self.properties:
            if p.required:
                required.append(p.name)
        obj["required"] = required

        spec = {}
        spec[self.name] = obj

        return spec

    def schemaSpecRef(self):
        return {"$ref": f"#/components/schemas/{self.name}"}
