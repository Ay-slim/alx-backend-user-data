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


class Auth:
    """
    Auth class to handle user authentication
    """
    def __init__(self):
        """Initialize auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """Registers a new user and validates password"""
        try:
            new_user = self._db.find_user_by(email=email)
            return new_user
        except Exception:
            hashedpw = _hash_password(password)
            return self._db.add_user(email, hashedpw)
