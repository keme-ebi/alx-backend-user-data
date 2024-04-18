#!/usr/bin/env python3
"""handles session ID expiration"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """inherits from SessionAuth and hadles the session ID expiration date"""
    def __init__(self):
        """initialization"""
        try:
            env = int(os.getenv("SESSION_DURATION"))
        except Exception:
            env = 0
        self.session_duration = env

    def create_session(self, user_id=None):
        """overloads create_session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overloads user_id_for_session_id"""
        if not session_id:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None
        if self.session_duration <= 0:
            return session.get('user_id')
        created_at = session.get('created_at')
        if not created_at:
            return None
        time = created_at + timedelta(seconds=self.session_duration)
        if time < datetime.now():
            return None
        return session.get('user_id')
