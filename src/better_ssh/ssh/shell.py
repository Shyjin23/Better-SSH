"""POSIX interactive SSH shell support."""

from __future__ import annotations

import os
import select
import sys
import termios
import tty

import paramiko


class InteractiveShell:
    """Run a basic POSIX terminal session over an SSH channel."""

    def __init__(self, client: paramiko.SSHClient) -> None:
        self.client = client


    def run(self) -> None:
        """Start the remote interactive shell."""
        
        channel = self.client.invoke_shell()
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setraw(sys.stdin.fileno())
            self._resize_channel(channel)

            while True:
                readable, _, _ = select.select([sys.stdin, channel], [], [])
                if sys.stdin in readable:
                    data = os.read(sys.stdin.fileno(), 1024)
                    if not data:
                        break
                    channel.send(data)

                if channel in readable:
                    data = channel.recv(4096)
                    if not data:
                        break
                    os.write(sys.stdout.fileno(), data)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            channel.close()


    @staticmethod
    def _resize_channel(channel: paramiko.Channel) -> None:
        """Match the remote PTY to the current terminal size when possible."""
        
        try:
            columns = os.get_terminal_size().columns
            rows = os.get_terminal_size().lines
        except OSError:
            return

        channel.resize_pty(width=columns, height=rows)
