#!/usr/bin/env python3
"""basic auth module"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic auth class"""
    pass
