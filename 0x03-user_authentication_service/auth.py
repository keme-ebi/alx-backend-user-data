#!/usr/bin/env python3
"""auth module"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string
    Arg:
        password(str): the password to hash
    Return:
        salted, hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user with mandatory email and password
        Args:
            email(str): user email
            password(str): user password
        Return:
            a User object
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user

        raise ValueError("User {} email already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """locates a user by email and checks if the password matches
        Args:
            email(str): user email to search for
            password(str): password to check
        Return:
            True if it matches, otherwise False
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False
        return False
