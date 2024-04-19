#!/usr/bin/env python3
"""session_db_auth"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """session database class"""
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        dic = {"user_id": user_id, "session_id": session_id}
        user = UserSession(**dic)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession in the database
            on session_id
        """
        if not session_id:
            return None
        # get user id from UserSession based on session_id
        try:
            user = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        # get session when a key is equal to session id
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None
        """ if session_duration is equal or under 10, return the
            user id from UserSession in the database
        """
        if self.session_duration <= 0:
            return user[0].user_id

        created_at = session.get('created_at')
        if not created_at:
            return None
        time = created_at + timedelta(seconds=self.session_duration)
        if time < datetime.now():
            return None
        # default
        return user[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID
            from the request cookie
        """
        if request is None:
            return False
        session = self.session_cookie(request)
        if not session:
            return False
        user = UserSession.search({"session_id": session_id})
        if not user:
            return False
        user[0].remove()
        return True
