#!/usr/bin/env python3
"""
AUTH session.
"""
from flask import request
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
        user_id_by_session_id[tmp] = user_id
        return tmp
