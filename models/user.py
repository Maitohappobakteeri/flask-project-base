from .base import Base
from .schema import Schema, Property, PropertyType

from sqlalchemy import Column, Integer, String
from flask_restful import fields


UserSchema = Schema(
    "User",
    [
        Property("id", PropertyType.integer),
        Property("username", PropertyType.string),
    ]
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
