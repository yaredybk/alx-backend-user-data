#!/usr/bin/env python3
"""0x00. Personal data
"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filter datum.

    Arguments:

    fields:    a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message:   a string representing the log line
    separator: a string representing by which character is separating all
               fields in the log line (message)
    """
    pattern = rf"({'|'.join(fields)})\=([^={separator}]*)"
    return re.sub(pattern, rf"\1={redaction}", message)
