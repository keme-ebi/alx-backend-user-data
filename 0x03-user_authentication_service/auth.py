#!/usr/bin/env python3
"""auth module"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


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

    def create_session(self, email: str) -> str:
        """finds a user with the email, and generates a new UUID
            and stores it in the database as the user's session_id
        Arg:
            email(str): user email to search for
        Return:
            the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """retrieves the corresponding User
        Arg:
            session_id(str): the session_id to retrieve user from
        Return:
            corresponding user, otherwise None
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user's session ID to None
        Arg:
            user_id(int): user id to update
        Return:
            None
        """
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """updates user's reset_token database field
        Arg:
            email(str): email to search for corresponding user
        Return:
            the generated token if user exists
            otherwise raise ValueError exception
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token
