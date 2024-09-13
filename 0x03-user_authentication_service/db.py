#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Any, Optional
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """create a user and return it"""
        u = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(u)
        session.commit()
        return u

    def find_user_by(self, **kwargs) -> User:
        """find user based on all kwargs

        Raises:
            InvalidRequestError if kwargs is None or
                                   has keys not in User class
        Returns:
            the first User match in db
        """
        if not kwargs:
            raise InvalidRequestError

        keys = set(kwargs.keys())
        user_cols = set(User.__table__.columns.keys())
        if not keys.issubset(user_cols):
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user_id with the provided kwargs"""
        user = self.find_user_by(id=user_id)

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
