# Better-SSH

A lightweight SSH/SCP client built for CTFs, labs, and experimentation.

## Features

- Connect to remote systems over SSH.
- Open an interactive remote shell.
- Upload and download files over SCP.
- Support password authentication and RSA private keys.
- Keep file operations under a single extensible `transfer` command.

## Requirements

- Python 3.12+
- An SSH server for remote connections.

## Installation

Clone the repository and install it in editable mode:

```bash
python -m pip install --editable ".[dev]"
```

## Usage

### Connect

```bash
better-ssh connect user@host
```

Specify a non-default SSH port:

```bash
better-ssh connect user@host --port 2222
```

Use an RSA private key:

```bash
better-ssh connect user@host --identity ~/.ssh/id_rsa
```

### Transfer files

The `transfer` command handles file operations through an action. This keeps
file transfer in one place and leaves room for additional actions later.

Upload a local file to the remote system:

```bash
better-ssh transfer user@host /local/file /remote/path --action upload
```

Download a remote file to the local system:

```bash
better-ssh transfer user@host /remote/file /local/path --action download
```

The same authentication options are available for transfers:

```bash
better-ssh transfer user@host /local/file /remote/path --action upload --port 2222
better-ssh transfer user@host /local/file /remote/path --action upload --identity ~/.ssh/id_rsa
```

## Project structure

```text
better-ssh/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── better_ssh/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── parsing.py
│       │   └── commands/
│       │       ├── __init__.py
│       │       ├── connect.py
│       │       └── transfer.py
│       └── ssh/
│           ├── __init__.py
│           ├── client.py
│           └── shell.py
├── tests/
│   ├── conftest.py
│   ├── cli/
│   │   ├── test_main.py
│   │   └── test_parsing.py
│   └── ssh/
│       └── test_client.py
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

## Development

Install the development dependencies:

```bash
python -m pip install --editable ".[dev]"
```

Run the test suite:

```bash
pytest
```

Run Ruff:

```bash
ruff check .
```

## Platform note

Interactive shell support currently targets POSIX systems. SSH connections and
file transfers do not require the local interactive shell functionality.
