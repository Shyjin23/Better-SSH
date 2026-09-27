from better_ssh.cli.parsing import parse_user_host


def test_parse_user_host() -> None:
    assert parse_user_host("alice@example.com") == ("alice", "example.com")


def test_parse_user_host_rejects_invalid_target() -> None:
    import pytest

    with pytest.raises(ValueError, match="user@host"):
        parse_user_host("example.com")
