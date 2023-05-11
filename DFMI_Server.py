import socket

def handler(host_ip, host_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_ip, host_port))
    print('[+] Awaiting Connection from Client...')
    sock.listen()
    remote_target, remote_ip = sock.accept()

    print(f'[+] Connection recieved from {remote_ip[0]}')

    while True:
        try:
            message = input('[>] Server Message to send #> ')
            remote_target.send(message.encode())

            if message == 'exit':
                remote_target.close()
                break

            response = remote_target.recv(1024).decode()
            print('[+] Message from client: \n' + response)

            if response == 'exit':
                print('[-] The client has terminated the session.')
                remote_target.close()
                break

        except KeyboardInterrupt:
            remote_target.close()
            print('[-] Interrupt issued, program exit.')
            break

        except Exception:
            sock.close()
            break

host_ip = '127.0.0.1'
host_port = 2222
handler(host_ip, host_port)
