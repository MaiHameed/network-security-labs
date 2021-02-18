from des import DesKey
import socket

HOST = 'localhost'
PORT = 9080
BUFFER = 1024

ida = b'INITIATOR A'
keym = DesKey(b'NETWORK SECURITY')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    
    # Sending cleartext of message 1
    s.sendall(ida)
    print('=== Sent ===')
    print(ida)

    # Received ciphertext of message 2
    e_keys = s.recv(BUFFER)
    e_ida = s.recv(BUFFER)
    e_idb = s.recv(BUFFER)
    print('=== Received Encrypted Messages ===')
    print(e_keys)
    print(e_ida)
    print(e_idb)

    # Decrypted message 2
    keys = keym.decrypt(e_keys, padding=True)
    ida = keym.decrypt(e_ida, padding=True)
    idb = keym.decrypt(e_idb, padding=True)
    print('=== Decrypted Messages Into ===')
    print(keys)
    print(ida)
    print(idb)

    # Sending ciphertext of message 3
    keys = DesKey(keys)
    e_idb = keys.encrypt(idb, padding=True)
    s.sendall(e_idb)
    print('=== Sent ===')
    print(e_idb)
    
    print('=== Disconnecting ===')
    s.close()
    exit()