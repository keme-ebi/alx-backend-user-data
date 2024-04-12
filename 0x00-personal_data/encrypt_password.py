#!/usr/bin/env python3
"""encrypt password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string
    Arg:
        password(str): the password to hash
    Return:
        salted, hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
