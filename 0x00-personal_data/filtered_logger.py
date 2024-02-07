#!/usr/bin/env python3
"""Mask personal details with regex"""


import re
from typing import List


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
