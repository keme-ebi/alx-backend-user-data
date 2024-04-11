#!/usr/bin/env python3
"""
filtered_logger module
"""
import re


def filter_datum(fields, redaction, message, separator):
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
    log = message
    for field in fields:
        pattern = r'(?<={}=).*?(?={}|$)'.format(field, re.escape(separator))
        log = re.sub(pattern, redaction, log)
    return log
