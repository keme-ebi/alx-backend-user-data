#!/usr/bin/env python3
"""manage API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """reurns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None
        Arg:
            request: the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        Arg:
            request: the Flask request object
        """
        return None
