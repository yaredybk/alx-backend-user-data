#!/usr/bin/env python3
"""
AUTH basic.
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """Auth class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require auth

        Returs:
            False
        """

    def authorization_header(self, request=None) -> str:
        """authorization header setter.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get curret user.
        """
        return None
