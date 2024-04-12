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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates that the provided password matches the hashed password
    Arg:
        hashed_password(bytes): the hashed password
        password: the password to check with
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
