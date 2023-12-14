#!/usr/bin/env python3 

import sys
import argparse
from client.client import SSH_Client 

# func to handle argument parsing
def parse_args(): 
    try:
        parser = argparse.ArgumentParser()
        sub_parsers = parser.add_subparsers(dest='action')

        connect_parser = sub_parsers.add_parser('connect')
        connect_parser.add_argument('-H', type=str, help="specify remote host", metavar=('user@host'))
        connect_parser.add_argument('-p', type=int, help="specify a port number", metavar=('port'), default=22)
        connect_parser.add_argument('-i', type=str, help="specify the path to a private key file", metavar=('pkey'))

        transfer_parser = sub_parsers.add_parser('transfer') 
        transfer_parser.add_argument('-p', type=int, help="specify a port number", metavar=('port'), default=22)
        transfer_parser.add_argument('-i', type=str, help="specify the path to a private key file", metavar=('pkey'))
        transfer_parser.add_argument('-x', type=str, choices=['put', 'pull'], help="specify the file transfer action: put / pull")
        transfer_parser.add_argument('f', nargs=2, help="specify the source and destination files for formatting", metavar=('file')) 

        return parser.parse_args()

    except Exception as e:
        if ']' in str(e):
            print(f"\n{str(e).split(']')[1][1:]}")
        else:
            print(f'\n{str(e)}') 

# Driver code
def main(): 
    args = parse_args() 

    ssh_client = SSH_Client()

    if args.action == 'connect': 
        password = None
        try:
            host = args.H.split('@')[1] 
            user = args.H.split('@')[0] 
        except Exception:
            print("\nHost-name cannot be recognised !")
            sys.exit(1) 
        if args.i is None:
            password = ssh_client.getpass(host, user) 
        client = ssh_client.establish_connection(host, args.p, user, password, args.i) 
        if client != None:
            ssh_client.open_shell(host, client)  
            sys.exit(0) 

    if args.action == 'transfer':
        password=None 
        if args.x == 'put':
            local_path, remote_path = args.f
            try:
                host = remote_path.split(':')[0].split('@')[1]
                user = remote_path.split('@')[0] 
                remote_path = remote_path.split(':')[1]
            except Exception:
                print("\nPlease specify files in the format: 'local_path user@host:remote_path'")
                sys.exit(1) 

        if args.x == 'pull':
            remote_path, local_path = args.f 
            try:
                host = remote_path.split(':')[0].split('@')[1] 
                user = remote_path.split('@')[0] 
                remote_path = remote_path.split(':')[1] 
            except Exception:
                print("\nPlease specify files in the format: 'user@host:remote_path local_path'")
                sys.exit(1)

        if args.i is None:
            password = ssh_client.getpass(host, user)
            client = ssh_client.establish_connection(host, args.p, user, password, args.i)
            if client != None:
                ssh_client.transfer(client, local_path, remote_path, args.x)
                sys.exit(0) 

if __name__ == '__main__':
    main() 

