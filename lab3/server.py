import socket
import select
import sys
import os
from des import DesKey
from time import sleep

HOST = 'localhost'
PORT = 9009
BUFFER = 1024



def startChatSession(conn, Ks):
    SOCKETS = [sys.stdin, conn]
    Ks = DesKey(Ks)

    while(1):
        readyToRead, [], [] = select.select(SOCKETS, [], [], 0)
        for sock in readyToRead:
            # Message in stdin
            if sock == sys.stdin:
                # Read in message from user in stdin
                # .rstrip removes trailing characters such as \n
                message = sock.readline().rstrip()
                
                # Check if user wants to quit
                if(message == 'q'):
                    print("Terminating chat session")
                    conn.close()
                    exit()
                
                # Encrypt and send message to server
                message = bytes(message,'utf-8')
                message = Ks.encrypt(message, padding=True)
                conn.sendall(message)

            # Message from client
            else:
                try:
                    receivedMessage = conn.recv(BUFFER)
                except:
                    print("Chat session terminated by client")
                    conn.close()
                    exit()

                # Terminate chat session if client terminated
                if (not receivedMessage):
                    print("Chat session terminated by client")
                    conn.close()
                    exit()
                
                receivedMessage = Ks.decrypt(receivedMessage, padding=True)
                print("Client: "+str(receivedMessage,'utf-8'))



def handleClient(conn):
    print("Establishing secure channel...")
    print(" ")

    clientPubKey = conn.recv(BUFFER)
    clientPubKey = DesKey(clientPubKey)
    print("Received client public key through public announcement")

    print("Sending server public key through public announcement")
    serverPubKey = b'pubKey S'
    conn.sendall(serverPubKey)
    serverPubKey = DesKey(serverPubKey)

    # Receive and decrypt client ID and nonce 1
    clientId = conn.recv(BUFFER)
    print("Received encrypted client ID as:")
    print(clientId)
    clientId = serverPubKey.decrypt(clientId, padding=True)
    print("Decrypted client ID to:")
    print(clientId)

    print("Received encrypted nonce as:")
    n1 = conn.recv(BUFFER)  
    print(n1)
    n1 = serverPubKey.decrypt(n1, padding=True)
    print("Decrypted nonce to:")
    print(n1)

    # Generating a new nonce to send to client
    print("Generating and encrypting nonce 2")
    n2 = b'N2'

    # Sending nonce 1 and newly generated nonce 2 to client
    print("Sending the encrypted nonces to the client")
    conn.sendall(clientPubKey.encrypt(n1, padding=True))
    conn.sendall(clientPubKey.encrypt(n2, padding=True))

    # Expecting nonce 2 from client
    n2_e = conn.recv(BUFFER)
    if(not n2_e):
        # Client terminated connection due to wrong authentication
        print("Connection error, try again")
        conn.close()
        exit()
    print("Received encrypted message:")
    print(n2_e)
    n2_e = serverPubKey.decrypt(n2_e, padding=True)
    if(n2 != n2_e):
        print("Expected nonce 2 from client but received:")
        print(n2_e)
        print("Terminating session...")
        conn.close()
        exit()
    print("Decrypted message to:")
    print(n2_e)

    # Expecting nonce 1 from client
    n1_e = conn.recv(BUFFER)
    if(not n1_e):
        # Client terminated connection due to wrong authentication
        print("Connection error, try again")
        conn.close()
        exit()
    print("Received encrypted message:")
    print(n1_e)
    n1_e = serverPubKey.decrypt(n1_e, padding=True)
    if(n1 != n1_e):
        print("Expected nonce 1 from client but received:")
        print(n1_e)
        print("Terminating session...")
        conn.close()
        exit()
    print("Decrypted message to:")
    print(n1_e)

    # Expecting session key from client
    Ks = conn.recv(BUFFER)
    print("Received encrypted message from client:")
    print(Ks)
    Ks = serverPubKey.decrypt(Ks, padding=True)
    print("Decrypted message into:")
    print(Ks)
    
    print(" ")
    print("Established secure channel, start chatting!")
    print("(Type 'q' at any time to quit)")
    startChatSession(conn, Ks)



# Opening a TCP connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Binds to the socket
    s.bind((HOST,PORT))
    s.listen()

    # continuously accepts incoming clients
    while 1:
        conn, addr = s.accept()
        # Check if incoming connection is a client or garbage
        data = conn.recv(BUFFER)
        if (data == b'client'):
            # Handle client connection
            print("Accepted client connection")
            handleClient(conn)