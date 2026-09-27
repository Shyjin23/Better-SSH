"""Helpers for parsing SSH and remote file arguments."""

from __future__ import annotations


def parse_user_host(value: str) -> tuple[str, str]:
    """Parse a ``user@host`` value."""
   
    if "@" not in value:
        raise ValueError("Target must be in the form user@host")

    username, hostname = value.split("@", 1)
    if not username or not hostname:
        raise ValueError("Target must be in the form user@host")

    return username, hostname
