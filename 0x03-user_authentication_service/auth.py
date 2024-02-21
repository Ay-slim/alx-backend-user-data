#!/usr/bin/env python3
"""User auth module """
import bcrypt
from typing import TypeVar
from uuid import uuid4

from db import DB


def _generate_uuid() -> str:
    """Generate a random uuid string"""
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Return true if login details are valid and false otherwise"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Generates a new session and returns its id"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """Fetches a user via session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Deletes a user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Password reset via token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        if user is None:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token
