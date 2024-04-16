#!/usr/bin/env python3
"""basic_auth module"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """inherits from the Auth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """returns the Base64 part of the Authorization header
        Arg:
            authorization_header: authorization header string
        """
        starts = "Basic "
        if not authorization_header or not type(authorization_header) == str:
            return None
        if not authorization_header.startswith(starts):
            return None
        value = authorization_header[len(starts):]
        return value

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a Base64 string
        Arg:
            base64_authorization_header: string to decode
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            dec = decoded.decode()
            return dec
        except Exception:
            return None
