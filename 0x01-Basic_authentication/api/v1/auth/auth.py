#!/usr/bin/env python3
"""Auth routes and views"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Class for auth ops"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Returns true for a present path
            Returns false for an excluded one
        """
        if excluded_paths is None or excluded_paths == [] or path is None:
            return True
        if path[-1] != '/':
            path += '/'
        for route in excluded_paths:
            if re.match(route.replace('*', '.*'), path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None for now to the header authorization """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None, will be the flask request object """
        return None
