#!/usr/bin/env python3
"""basic_auth module"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> str:
        """returns the user email and password from the decoded value
        Arg:
            decoded_base64_authorization_header: Base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        splited = decoded_base64_authorization_header.split(":")
        email, user_pwd = splited[0], splited[1]
        return email, user_pwd

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> str:
        """returns the User instance based on the email and password
        Args:
            user_email(str): user email
            user_pwd(str): user password
        Return:
            instance of the User
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        autho_header = self.authorization_header(request)
        if autho_header:
            header = self.extract_base64_authorization_header(autho_header)
            dec_header = self.decode_base64_authorization_header(header)
            email, pwd = self.extract_user_credentials(dec_header)
            user = self.user_object_from_credentials(email, pwd)
            return user
        return
