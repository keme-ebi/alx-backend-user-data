#!/usr/bin/env python3
"""
filtered_logger module
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that returns the log message obfuscated
    The function uses regex to replace occurences of certain field values
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing by which character is separating
            all fields in the log
    Return:
        the log message obfuscated
    """
    for field in fields:
        pattern = r'(?<={}=).*?(?={}|$)'.format(field, separator)
        message = re.sub(pattern, redaction, message)
    return message
