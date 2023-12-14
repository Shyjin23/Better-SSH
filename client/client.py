import os 
import sys
import tty  
import socket
import select
import getpass
import termios 
import paramiko  
import subprocess 
from scp import SCPClient 

class SSH_Client: 

    # func to receive password from user without echo
    def getpass(self, host, user):
        return getpass.getpass(prompt=f"{user}@{host}'s password: ", stream=None)  

    # func to instantiate an connection with the remote server
    def establish_connection(self, host, port, user, password, pkey): 
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:  
            if pkey is None:
                client.connect(host, port=port, username=user, password=password) 
                return client 
            else:
                try:
                    pkey = paramiko.RSAKey.from_private_key_file(pkey)  
                    client.connect(host, port=port, username=user, pkey=pkey) 
                    return client 
                except paramiko.ssh_exception.PasswordRequiredException:
                    passphrase = getpass.getpass(prompt=f"Enter passphrase for key '{pkey}': ",stream=None) 
                    pkey = paramiko.RSAKey.from_private_key_file(pkey, password=passphrase)
                    client.connect(host, port=port, username=user, pkey=pkey)
                    return client

        except Exception as e:
            if ']' in str(e): 
                print(f"\n{str(e).split(']')[1][1:]}")
            else:
                print(f'\n{str(e)}')

        return 
        
    # func to open channel for interactive shell communication 
    def open_shell(self, host, client):

        def resize_pty(channel):
            tty_height, tty_width = subprocess.check_output(['stty', 'size']).split()

            try:
                channel.resize_pty(width=int(tty_width), height=int(tty_height))
            except paramiko.ssh_exception.SSHException:
                pass
 
        sys.stdout.write('\n')
        sys.stdout.flush() 
        oldtty_attrs = termios.tcgetattr(sys.stdin)
        with client.invoke_shell() as channel:
            try:
                stdin_fileno = sys.stdin.fileno()
                tty.setraw(stdin_fileno)
                tty.setcbreak(stdin_fileno)
                channel.settimeout(0.0)
                is_alive = True

                while is_alive:
                    resize_pty(channel)
                    read_ready, write_ready, exception_list = select.select([channel, sys.stdin], [], [])

                    if channel in read_ready:
                        try:
                            out = channel.recv(1024)
                            if len(out) == 0:
                                is_alive = False
                            else:
                                print(f"{out.decode()}", end='')
                                sys.stdout.flush()
                        except socket.timeout:
                            pass

                    if sys.stdin in read_ready and is_alive:
                        char = os.read(stdin_fileno, 1)
                        if len(char) == 0:
                            is_alive = False
                        else:
                            channel.send(char)

            except Exception as e:
                if ']' in str(e):
                    print(f"\n{str(e).split(']')[1][1:]}")
                else:
                    print(f'\n{str(e)}')

            finally:  
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, oldtty_attrs)  
                print(f"\nConnection to {host} closed !") 
        client.close()
        return 

    # func to handle file transfers
    def transfer(self, client, local_path, remote_path, action):
        def progress(filename, size, sent):
            sys.stdout.write("\r%s's progress: %.2f%%   " % (filename.decode(), float(sent) / float(size) * 100))
            sys.stdout.flush()

        try:
            with SCPClient(client.get_transport(), progress=progress) as scp:
                sys.stdout.write('\n')
                sys.stdout.flush()

                if action == 'pull':
                    scp.get(remote_path, local_path)
                    sys.stdout.write('\rFile Downloaded Successfully !          \n')
                    sys.stdout.flush()

                if action == 'put':
                    scp.put(local_path, remote_path)
                    sys.stdout.write('\rFile Uploaded Successfully !          \n')
                    sys.stdout.flush()

        except Exception as e:
            if ']' in str(e):
                print(f"\n{str(e).split(']')[1][1:]}")
            else:
                print(f'\n{str(e)}')

        finally:
            client.close() 
            return 

