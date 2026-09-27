"""Implementation of the transfer command."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from better_ssh.cli.parsing import parse_user_host
from better_ssh.ssh.client import SSHClient


def run_transfer(args: Namespace) -> None:
    """Upload or download a file."""
    username, hostname = parse_user_host(args.target)

    client = SSHClient(
        hostname=hostname,
        username=username,
        port=args.port,
        identity_file=Path(args.identity) if args.identity else None,
    )

    try:
        client.connect()
        if args.action == "upload":
            client.upload(args.source, args.destination)
        else:
            client.download(args.source, args.destination)
    finally:
        client.close()
