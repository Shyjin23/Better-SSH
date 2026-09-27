"""SSH and SCP client functionality."""

from __future__ import annotations

import os
from getpass import getpass
from pathlib import Path
from typing import Any

import paramiko
from scp import SCPClient as SCPTransferClient


class SSHClient:
    """Small wrapper around Paramiko and SCP for the CLI."""

    def __init__(
            self, 
            hostname: str, 
            username: str, 
            port: int = 22, 
            identity_file: Path | None = None
        ) -> None:

        self.hostname = hostname
        self.username = username
        self.port = port
        self.identity_file = identity_file
        self._client: paramiko.SSHClient | None = None


    def connect(self) -> None:
        """Establish an SSH connection."""
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs: dict[str, Any] = {
            "hostname": self.hostname,
            "port": self.port,
            "username": self.username,
            "timeout": 10,
        }

        if self.identity_file is not None:
            key = self._load_private_key(self.identity_file)
            connect_kwargs["pkey"] = key
        else:
            connect_kwargs["password"] = getpass("Password: ")

        client.connect(**connect_kwargs)
        self._client = client


    def open_shell(self) -> None:
        """Open an interactive shell over the SSH connection."""

        if os.name == "nt":
            raise RuntimeError("Interactive shell is currently supported on POSIX only")

        
        if self._client is None:
            raise RuntimeError("SSH client is not connected")

        from better_ssh.ssh.shell import InteractiveShell

        InteractiveShell(self._client).run()


    def upload(self, source: str, destination: str) -> None:
        """Upload a local file to the remote system."""
        
        client = self._require_connection()
        with SCPTransferClient(client.get_transport()) as scp_client:
            scp_client.put(source, destination)


    def download(self, source: str, destination: str) -> None:
        """Download a remote file to the local system."""
        
        client = self._require_connection()
        with SCPTransferClient(client.get_transport()) as scp_client:
            scp_client.get(source, destination)


    def close(self) -> None:
        """Close the SSH connection."""
        
        if self._client is not None:
            self._client.close()
            self._client = None


    def _require_connection(self) -> paramiko.SSHClient:
        """Return the active SSH client or raise if not connected."""

        if self._client is None:
            raise RuntimeError("SSH client is not connected")
        return self._client


    @staticmethod
    def _load_private_key(path: Path) -> paramiko.RSAKey:
        """Load an RSA private key, prompting for a passphrase when needed."""
       
        try:
            return paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            passphrase = getpass("Key passphrase: ")
            return paramiko.RSAKey.from_private_key_file(
                path,
                password=passphrase,
            )
