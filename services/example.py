from .service import Service, current_user_id
from models.example import Example

import datetime


class ExampleService(Service):
    def __init__(self, session):
        super().__init__(session)

    def new(self, message):
        example = Example(
            owner=current_user_id(),
            message=message,
            created_at=datetime.datetime.utcnow(),
        )

        self._session.add(example)
        self._session.commit()
        return example

    def edit(self, exampleId, message):
        example = self.example(exampleId)
        example.message = message
        return example

    def example(self, exampleId):
        return self._query(Example).get(exampleId)

    def history(self, start, amount):
        return self._query(Example) \
                   .filter(Example.owner == current_user_id()) \
                   .order_by(Example.created_at.desc()) \
                   .offset(start) \
                   .limit(amount) \
                   .all()
