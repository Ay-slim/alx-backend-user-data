#!/usr/bin/env python3
"""Mask personal details with regex"""


import re
import logging
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filter_datum - Filter data and replace with obfuscation
    @fields: Fields to redact
    @redaction: String to redact with
    @message: Message to redact
    @separator: Message separator
    Returns: String with obfuscated text
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction + separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields,
                            self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Accepts no arguments and returns a logging.Logger object
    """
    log_object = logging.getLogger("user_data")
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    log_object.setLevel(logging.INFO)
    log_object.propagate = False
    log_object.addHandler(stream)
    return log_object
