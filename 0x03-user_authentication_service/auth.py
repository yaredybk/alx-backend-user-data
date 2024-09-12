#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from uuid import uuid4


def _hash_password(password: str) -> str:
    """generate a salted hash of the input password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    UUID = uuid4()
    return str(UUID)
