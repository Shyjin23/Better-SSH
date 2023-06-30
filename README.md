
¥ This is a command-line SSH client implemented in Python using the Paramiko library. 

### Features :

- Connect to remote hosts using SSH with password authentication or private key authentication.
- Transfer files to and from remote servers securely using SCP.
- Open an interactive shell session on the remote server. 

### Prerequisites :

- Python 3.x
- Paramiko library
- SCP library 

### Usage :

To use the SSH client, clone this repository, navigate to the project directory and run the `main.py` file with the desired command-line arguments.

##### Connect to a remote server :

To connect to a remote server, use the `connect` command:

```
./main.py connect -H <user@host> [-p <port>] [-i <private_key>] 

Eg: ./main.py connect -H user@127.0.0.1 
```

`<user@host>`: Specify the username and hostname of the remote server.

`<port>` (optional): Specify the SSH port number. Default is 22.

`<private_key>` (optional): Specify the path to a private key file for authentication.

##### Transfer files :

To transfer files to or from a remote server, use the `transfer` command:

```
./main.py transfer [-p <port>] [-i <private_key>] -x <action> <source_file> <destination_file> 

Eg: ./main.py transfer -x put ./file1.txt user@127.0.0.1:/tmp
```

`<action>`: Specify the file transfer action: put (upload file to remote server) or pull (download file from remote server).

`<source_file>`: Specify the source file for transfer.

`<destination_file>`: Specify the destination file for transfer. 

