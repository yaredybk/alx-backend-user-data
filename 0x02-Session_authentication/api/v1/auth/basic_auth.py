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
        pattern = r'Basic (?P<token>.+)'
        field_match = re.fullmatch(pattern, authorization_header.strip())
        if field_match is not None:
            return field_match.group('token')
        return None

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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """user email and password from the Base64 decoded value."""
        if type(decoded_base64_authorization_header) == str:
            p = r'([^:]*):(.*)'
            match = re.match(p, decoded_base64_authorization_header)
            if match:
                return match.groups()
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
