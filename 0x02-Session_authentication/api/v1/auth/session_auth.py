#!/usr/bin/env python3
"""
AUTH session.
"""
from flask import request
from models.user import User
import re
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session Auth class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        tmp = uuid4()
        self.user_id_by_session_id[tmp] = user_id
        return tmp

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get a User ID based on a Session ID:"""
        if session_id is None or type(session_id) is not str:
            return None
        return user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """GET a User instance based on a cookie value."""
        c = self.session_cookie(request)
        user_id  = self.user_id_for_session_id(c)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete the user session / logout."""
        cookie = self.session_cookie(request)
        if request is None or cookie is None:
            return False
        user_id = self.user_id_for_session_id(cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
