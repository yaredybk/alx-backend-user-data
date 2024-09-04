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

        Returns.
            True if path is None
            True if excluded_paths is None or empty
            False if path is in excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            p = rf"^{p.replace('/$', "")}"
            path = path.replace('/$', "")
            m = path.match(p)
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
