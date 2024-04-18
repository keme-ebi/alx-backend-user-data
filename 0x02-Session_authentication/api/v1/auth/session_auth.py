#!/usr/bin/env python3
"""SessionAuth
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """class that inherits from Auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a user_id
        Arg:
            user_id(str): the user id to create a session ID for
        Return:
            the session ID
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user ID based on a session ID
        Arg:
            session_id(str): session ID to check for user ID
        Return:
            user ID
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value
        Arg:
            request: Flask object
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes a user session/logout
        Arg:
            request: Flask object
        """
        if not request:
            return False
        session = self.session_cookie(request)
        if not session:
            return False
        if not self.user_id_for_session_id(session):
            return None
        del self.user_id_by_session_id[session]
        return True
