from des import DesKey
import socket

HOST = 'localhost'
PORT = 9060
BUFFER = 1024

ida = b'INITIATOR A'
key = DesKey(b'NETWORK SECURITY')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(ida)
    print('Sent the following data to the responder: ', ida)
    data = s.recv(BUFFER)

print('Received ',repr(data))