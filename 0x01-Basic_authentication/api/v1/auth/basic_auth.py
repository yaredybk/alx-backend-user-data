#!/usr/bin/env python3
""" Basic auth.
"""
from api.v1.auth.auth import Auth
import re
import base64
import binascii
from typing import Tuple, TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic auth class. """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header.

        for a Basic Authentication:
        """
        if authorization_header is None or \
                type(authorization_header) is not str or \
                not authorization_header.startswith("Basic"):
            return None
        return re.sub(r'(Basic )(*)', r'\2', authorization_header)

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode base64-encoded authorization header.
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
