from .base import Base
from .schema import Schema, Property, PropertyType

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)

MyExampleSchema = Schema(
    "MyExample",
    [
        Property("id", PropertyType.integer),
        Property("message", PropertyType.string),
        Property("created_at", PropertyType.datetime),
    ]
)

NewExampleSchema = Schema(
    "NewExample",
    [
        Property("message", PropertyType.string),
    ]
)


class Example(Base):
    __tablename__ = 'example'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(String(256), nullable=False)
    created_at = Column(DateTime, nullable=False)
