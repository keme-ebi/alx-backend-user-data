#!/usr/bin/env python3
"""
filtered_logger module
"""
import logging
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """instance initialization"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        message = super(RedactingFormatter, self).format(record)
        return (filter_datum(self.fields, RedactingFormatter.REDACTION,
                             message, RedactingFormatter.SEPARATOR))


def get_logger() -> logging.Logger:
    """function that returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
