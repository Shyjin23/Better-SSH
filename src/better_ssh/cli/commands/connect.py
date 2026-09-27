"""Implementation of the connect command."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from better_ssh.cli.parsing import parse_user_host
from better_ssh.ssh.client import SSHClient


def run_connect(args: Namespace) -> None:
    """Connect to a host and open an interactive shell."""
    
    username, hostname = parse_user_host(args.target)

    client = SSHClient(
        hostname=hostname,
        username=username,
        port=args.port,
        identity_file=Path(args.identity) if args.identity else None,
    )

    try:
        client.connect()
        client.open_shell()
    finally:
        client.close()
