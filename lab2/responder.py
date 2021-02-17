from des import DesKey
import socket

HOST = 'localhost'
PORT = 9060
BUFFER = 1024

ida = b'INITIATOR A'
idb = b'RESPONDER B'
key = DesKey(b'NETWORK SECURITY')

# Encrypted plaintext
e_idb = key.encrypt(idb, padding=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    while 1:
        conn, addr = s.accept()
        with conn:
                print(addr,' is currently connected')
                while 1:
                    data = conn.recv(BUFFER)
                    if not data:
                        print(addr,' disconnected')
                        break
                    print('Received: ', data)
                    if (data == ida):
                        print('Received: ', data)
                        print('Established connection with initiator')
                        
