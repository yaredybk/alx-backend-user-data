#!/usr/bin/env python3
"""0x00. Personal data
"""
import logging
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format list of fields."""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """Create logger objec. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(sh)
    return logger
