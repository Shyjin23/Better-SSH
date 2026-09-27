# Better-SSH

A lightweight Python SSH/SCP client for CTFs, labs, and experimentation.

Better-SSH provides a simple command-line interface for connecting to remote systems over SSH and transferring files over SCP.

## Features

* Connect to remote systems over SSH.
* Open an interactive remote shell.
* Upload files to remote systems.
* Download files from remote systems.
* Support password authentication.
* Support RSA private key authentication.
* Keep SSH and file-transfer operations under a simple CLI.
* Designed to be lightweight and easy to extend.

## Requirements

* Python 3.12+
* An accessible SSH server for remote connections.

## Installation

Clone the repository and install the project in editable mode:

```bash
git clone https://github.com/<username>/Better-SSH.git
cd Better-SSH

python -m pip install -e .
```

For development, install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Run the CLI with:

```bash
better-ssh --help
```

### SSH Connection

Connect to a remote SSH server:

```bash
better-ssh connect <host> -u <username>
```

Depending on the authentication method, you can provide a password or RSA private key.

### File Transfer

File operations are handled through the `transfer` command.

Upload a file:

```bash
better-ssh transfer upload <local-file> <remote-path>
```

Download a file:

```bash
better-ssh transfer download <remote-file> <local-path>
```

Use:

```bash
better-ssh transfer --help
```

for the currently supported options.

> **Note:** The exact command-line options may change as the project develops. Use `--help` for the authoritative list of available commands and options.


## Project Structure

The project follows a simple, module-oriented structure:

```text
Better-SSH/
├── src/
│   └── better_ssh/
│       ├── cli/
│       │   ├── commands/
│       │   └── main.py
│       ├── ssh/
│       └── ...
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

The implementation is kept modular so that SSH functionality, file transfers, and CLI commands can evolve independently without introducing unnecessary abstraction.

## Development

Clone the repository and install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the test suite with:

```bash
pytest
```

## Project Goals

Better-SSH is primarily an educational and practical project intended for:

* CTF environments.
* SSH experimentation.
* Learning Python networking and CLI development.
* Building small security-focused utilities.

The project intentionally favors straightforward implementations over unnecessary complexity.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
