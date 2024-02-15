#!/usr/bin/env python3
""" Session auth module """
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ INitiate user session"""
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user session id """

        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns user instance from cookies value"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroys user session """
        if request is None:
            return False
        cookies = self.session_cookie(request)
        if cookies is None or cookies == '':
            return False
        if self.user_id_for_session_id(cookies) is None:
            return False
        del self.user_id_by_session_id[cookies]
        return True
