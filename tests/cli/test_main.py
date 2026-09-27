from better_ssh.cli.main import build_parser


def test_transfer_parser_supports_upload() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "transfer",
            "user@host",
            "/local/file",
            "/remote/file",
            "--action",
            "upload",
        ]
    )

    assert args.command == "transfer"
    assert args.action == "upload"


def test_transfer_parser_supports_download() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "transfer",
            "user@host",
            "/remote/file",
            "/local/file",
            "--action",
            "download",
        ]
    )

    assert args.action == "download"
