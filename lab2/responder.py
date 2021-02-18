from des import DesKey
import socket
from time import sleep

HOST = 'localhost'
PORT = 9080
BUFFER = 1024

# Plaintext messages
ida = b'INITIATOR A'
idb = b'RESPONDER B'
keym = DesKey(b'NETWORK SECURITY')
keys = b'RYERSON ' # Key must be 8 bytes long

# Encrypted plaintext
e_keys = keym.encrypt(keys, padding=True)
e_ida = keym.encrypt(ida, padding=True)
e_idb = keym.encrypt(idb, padding=True)

# Opening a TCP connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Binds to the socket
    s.bind((HOST,PORT))
    s.listen()
    # continuously accepts incoming clients
    while 1:
        conn, addr = s.accept()
        with conn:
            print(addr,' is currently connected')
            while 1:
                # waits for incoming data from the connected client
                data = conn.recv(BUFFER)
                if not data:
                    print(addr,' disconnected')
                    break
                # checks to see if the client is ID-a
                elif (data == ida):
                    # Received message 1
                    print('=== Received ===')
                    print(data)

                    # Sending ciphertext of message 2
                    conn.sendall(e_keys)
                    sleep(0.01) # Adding delays to prevent mismatch of message sending
                    conn.sendall(e_ida)
                    sleep(0.01)
                    conn.sendall(e_idb)
                    print('=== Sent ===')
                    print(e_keys)
                    print(e_ida)
                    print(e_idb)

                    # Received ciphertext of message 3
                    data = conn.recv(BUFFER)
                    print('=== Received ===')
                    print(data)

                    # Decrypted message 3
                    keys = DesKey(keys)
                    data = keys.decrypt(data, padding=True)
                    print('=== Decrypted ===')
                    print(data)

                    print('=== Disconnecting ===')
                    s.close()
                    exit()
                else:
                    break