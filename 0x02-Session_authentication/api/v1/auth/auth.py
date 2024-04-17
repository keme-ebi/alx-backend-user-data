#!/usr/bin/env python3
"""manage API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns true if the path is not in the list of excluded_paths
        Args:
            path: the path to check
            excluded_paths: a list of excluded paths
        Return:
            True if path no in excluded_paths, otherwise False
        """
        if not path or not excluded_paths:
            return True
        if not path.endswith("/"):
            path += "/"
        for p in excluded_paths:
            if p.endswith("*"):
                if path.startswith(p[:-1]):
                    return False
            else:
                if path == p:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns the value of the header request Authorization
        Arg:
            request: the Flask request object
        Return:
            value request Authorization if request contains the header key,
            otherwise None
        """
        if not request or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        Arg:
            request: the Flask request object
        """
        return None
