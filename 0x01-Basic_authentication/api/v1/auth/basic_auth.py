#!/usr/bin/env python3
"""basic_auth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """inherits from the Auth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """returns the Base64 part of the Authorization header"""
        starts = "Basic "
        if not authorization_header or not type(authorization_header) == str:
            return None
        if not authorization_header.startswith(starts):
            return None
        value = authorization_header[len(starts):]
        return value
