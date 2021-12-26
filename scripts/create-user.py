import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ..db import session_scope
from ..services.user import UserService


def main():
    username = sys.argv[1]
    password = sys.argv[2]
    with session_scope() as session:
        userService = UserService(session)
        userService.createUser(username, password, False)


if __name__ == "__main__":
    main()
