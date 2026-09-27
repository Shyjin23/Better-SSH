from unittest.mock import MagicMock, patch

from better_ssh.ssh.client import SSHClient


def test_upload_uses_scp_put() -> None:
    ssh_client = SSHClient("host", "user")
    ssh_client._client = MagicMock()
    transport = ssh_client._client.get_transport.return_value

    with patch("better_ssh.ssh.client.SCPTransferClient") as scp_class:
        scp_instance = scp_class.return_value.__enter__.return_value
        ssh_client.upload("local.txt", "/tmp/remote.txt")

    scp_class.assert_called_once_with(transport)
    scp_instance.put.assert_called_once_with("local.txt", "/tmp/remote.txt")


def test_download_uses_scp_get() -> None:
    ssh_client = SSHClient("host", "user")
    ssh_client._client = MagicMock()
    transport = ssh_client._client.get_transport.return_value

    with patch("better_ssh.ssh.client.SCPTransferClient") as scp_class:
        scp_instance = scp_class.return_value.__enter__.return_value
        ssh_client.download("/tmp/remote.txt", "local.txt")

    scp_class.assert_called_once_with(transport)
    scp_instance.get.assert_called_once_with("/tmp/remote.txt", "local.txt")
