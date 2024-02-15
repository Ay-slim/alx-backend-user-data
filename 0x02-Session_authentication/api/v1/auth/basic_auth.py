#!/usr/bin/env python3
"""basic auth module"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            Returns auth header
        """
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """REturn a decoded base 64 auth value"""

        if type(base64_authorization_header) is not str:
            return None
        try:
            code = base64.b64decode(
                base64_authorization_header
            )
            return code.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """pulls email and password from encoded string"""
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
            Construct user instance from uname and pw
        """
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Fetches user instance from a request"""

        head = self.authorization_header(request)
        if head is None:
            return None
        extract = self.extract_base64_authorization_header(head)
        if extract is None:
            return None
        decoded = self.decode_base64_authorization_header(extract)
        if decoded is None:
            return None
        credentials = self.extract_user_credentials(decoded)
        if credentials is None:
            return None
        user = self.user_object_from_credentials(
            credentials[0],
            credentials[1]
        )
        return user
