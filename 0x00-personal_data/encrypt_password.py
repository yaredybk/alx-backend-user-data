#!/usr/bin/env python3
"""Hash/Salt Password."""
import bcrypt


def hash_password(password : str) -> bytes:
    """Hash and Salt password

    Returns:
        a string
    """
    if password:
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Use bcrypt to validate that the provided password
    matches the hashed password.

    Arguments:
        hashed_password: bytes type
        password: string type
    Returns:
        bool: True if valid else false
    """
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)
