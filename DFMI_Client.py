import socket

def handler():
    print(f'[+] Connecting to {host_ip}.')
    sock.connect((host_ip, host_port))
    print(f'[+] Connected to {host_ip}.')

    while True:
        try:
            print('[+] Awaiting response...')
            message = sock.recv(1024).decode()
            print('[+] Message from server: ' + message)

            if message == 'exit':
                print('[-] The server has terminated the session.')
                sock.close()
                break

            response = input('[>] Client Message to send #> ')
            sock.send(response.encode())

            if response == 'exit':
                remote_target.close()
                break

        except KeyboardInterrupt:
            sock.close()
            print('[-] Interrupt issued, program exit.')
            break

        except Exception:
            sock.close()
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1'
host_port = 2222
handler()