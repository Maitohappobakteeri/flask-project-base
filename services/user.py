from .service import Service, current_user_id
from models.user import User

from werkzeug.security import generate_password_hash


class UserService(Service):
    def __init__(self, session):
        super().__init__(session)

    def current(self):
        return self._query(User).get(current_user_id())

    def userWithUsername(self, username):
        return self._query(User) \
                   .filter(User.username == username) \
                   .first()

    def createUser(self, username, password, isAdmin):
        hash = generate_password_hash(password)
        newUser = User(username=username, password=hash)
        self._session.add(newUser)
