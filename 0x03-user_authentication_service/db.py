#!/usr/bin/env python3
"""DB module
"""
from typing import Mapping
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add_user - Adds a new user
        @email: User email
        @hashed_password: User hashed password
        Return: Retunrs the new user object
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs: Mapping) -> User:
        """
        find_user_by - Find user by any attr
        @kwargs: Variable collection of db properties
        Returns: User who fits args
        """
        all_users = self._session.query(User)
        if not all_users:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError
        matching_user = self._session.query(User).filter_by(**kwargs).first()
        if not matching_user:
            raise NoResultFound
        return matching_user

    def update_user(self, user_id: int, **kwargs: Mapping) -> None:
        """
        update_user - Update user with given values
        """
        matched_user = self.find_user_by(id=user_id)
        if matched_user:
            valid_keys = [
                    'id', 'email',
                    'hashed_password',
                    'session_id', 'reset_token']
            for key, val in kwargs.items():
                if key not in valid_keys:
                    raise ValueError
                setattr(matched_user, key, val)
        self._session.add(matched_user)
        self._session.commit()
