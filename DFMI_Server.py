###########################################################################################
# Author:      Seth J. Gibson
# Course:      Learn by Doing - Python3 Command and Control How To Guide, by Joe Helle
# Program:     Don't Fence Me In
# Description: This program is the server for a C2 I am writing in my free time, following
#                   the guidance of Joe Helle's C2 course. This is primarily a learning
#                   experience for building large-scale projects, along with developing an 
#                   understanding of C2 malware and a further understanding of Python 
#                   Socket applications.
# Theme Song:   https://www.youtube.com/watch?v=3abZal0fXCU&ab_channel=MichaelWyckoff
# Changelog:    Added command-line arguments for IP and PORT
#               Split sections of handler() into subfunctions
#               Added fancy new banner
###########################################################################################

import socket
import sys

buffer_size = 1024

def banner():
    print('\n██████╗  ██████╗ ███╗   ██╗████████╗    ███████╗███████╗███╗   ██╗ ██████╗███████╗    ███╗   ███╗███████╗    ██╗███╗   ██╗')
    print('██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝    ██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝    ████╗ ████║██╔════╝    ██║████╗  ██║')
    print('██║  ██║██║   ██║██╔██╗ ██║   ██║       █████╗  █████╗  ██╔██╗ ██║██║     █████╗      ██╔████╔██║█████╗      ██║██╔██╗ ██║')
    print('██║  ██║██║   ██║██║╚██╗██║   ██║       ██╔══╝  ██╔══╝  ██║╚██╗██║██║     ██╔══╝      ██║╚██╔╝██║██╔══╝      ██║██║╚██╗██║')
    print('██████╔╝╚██████╔╝██║ ╚████║   ██║       ██║     ███████╗██║ ╚████║╚██████╗███████╗    ██║ ╚═╝ ██║███████╗    ██║██║ ╚████║')
    print('╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝       ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝╚══════╝    ╚═╝╚═╝  ╚═══╝')
    print('                                                                                                    by Seth Gibson        ')

def comm_in(remote_target):
    print('[+] Awaiting response...')
    response = remote_target.recv(buffer_size).decode()
    return response

def comm_out(remote_target, message):
    remote_target.send(message.encode())

def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting Connection from Client...')
    sock.listen()
    remote_target, remote_ip = sock.accept()
    comm_handler(remote_target, remote_ip)

def comm_handler(remote_target, remote_ip):
    print(f'[+] Connection recieved from {remote_ip[0]}')

    while True:
        try:
            message = input('[>] Server Message to send #> ')
            remote_target.send(message.encode())

            if message == 'exit':
                remote_target.close()
                break

            response = remote_target.recv(buffer_size).decode()
            print('[+] Message from client: \n' + response)

            if response == 'exit':
                print('[-] The client has terminated the session.')
                remote_target.close()
                break

        except KeyboardInterrupt:
            remote_target.close()
            print('\n[-] Interrupt issued, program exit.')
            break

        except Exception:
            remote_target.close()
            break

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = sys.argv[1]
    host_port = int(sys.argv[2])
    banner()
    listener_handler()
