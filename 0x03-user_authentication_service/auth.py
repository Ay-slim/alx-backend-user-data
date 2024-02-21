#!/usr/bin/env python3
"""User auth module """
import bcrypt
from typing import TypeVar
from uuid import uuid4

from db import DB


def _hash_password(password: str) -> bytes:
    """
    Returns the hashed version of a password
    """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
