"""Argument parser and entry point for Better-SSH."""

from __future__ import annotations

import argparse

from better_ssh import __version__
from better_ssh.cli.commands.connect import run_connect
from better_ssh.cli.commands.transfer import run_transfer


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="better-ssh",
        description="A lightweight SSH/SCP client built for CTFs, labs, "
        "and experimentation.",
    )
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest="command", required=True)

    connect = subparsers.add_parser("connect", help="Connect to a remote host")
    connect.add_argument("target", help="Remote target in the form user@host")
    _add_connection_options(connect)
    connect.set_defaults(handler=run_connect)

    transfer = subparsers.add_parser(
        "transfer",
        help="Upload or download files",
    )
    transfer.add_argument(
        "target",
        help="Remote target in the form user@host",
    )
    transfer.add_argument(
        "source",
        help="Local or remote file path, depending on the action",
    )
    transfer.add_argument(
        "destination",
        help="Destination file path",
    )
    transfer.add_argument(
        "-x",
        "--action",
        choices=("upload", "download"),
        required=True,
        help="Transfer action to perform",
    )
    _add_connection_options(transfer)
    transfer.set_defaults(handler=run_transfer)

    return parser


def _add_connection_options(parser: argparse.ArgumentParser) -> None:
    """Add options shared by SSH commands."""
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=22,
        help="SSH port (default: 22)",
    )
    parser.add_argument(
        "-i",
        "--identity",
        help="Path to an RSA private key",
    )


def main() -> None:
    """Run the Better-SSH command-line interface."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.handler(args)
    except ValueError as exc:
        parser.error(str(exc))
