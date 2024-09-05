#!/usr/bin/env python3
"""
AUTH basic.
"""
from flask import request
from os import getenv
import re
from typing import List, TypeVar


class Auth:
    """Auth class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require auth

        Returns.
            True if path is None
            True if excluded_paths is None or empty
            False if path is in excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            p = re.sub(r'/$|\*$',
                       lambda m: '' if m.group() == '/' else '.*',
                       p)
            p = f"^{p}$"
            path = re.sub(r"/$", "", path)
            m = re.match(p, path)
            if m:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header / None if does not exit.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Get curret user.
        """
        return None

    def session_cookie(self, request=None):
        """Get a cookie value from a request."""
        if request is None:
            return None
        return request.cookies.get(getenv("SESSION_NAME"))
