from des import DesKey
from time import sleep
import socket
import select
import sys
import os

HOST = 'localhost'
PORT = 9009
BUFFER = 1024

# Client public key
clientPubKey = b'pubKey C'

# Session Key
Ks = b'sessionk'



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
            
            # Message from server
            else:
                try:
                    receivedMessage = conn.recv(BUFFER)
                except:
                    print("Chat session terminated by server")
                    conn.close()
                    exit()

                # Terminate chat session if server terminated
                if (not receivedMessage):
                    print("Chat session terminated by server")
                    conn.close()
                    exit()
                
                receivedMessage = Ks.decrypt(receivedMessage, padding=True)
                print("Server: "+str(receivedMessage,'utf-8'))



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    # Sends verification so the server knows its a client
    # and not a random garbage connection
    s.sendall(b'client')
    sleep(0.01)

    print("Established connection to the server")
    print("Establishing secure channel...")
    print(" ")

    # Public announcement of public key
    print("Sending public key to server")
    s.sendall(clientPubKey)
    clientPubKey = DesKey(clientPubKey)

    # Accept server public key
    print("Waiting for the server public key")
    serverPubKey = s.recv(BUFFER)
    serverPubKey = DesKey(serverPubKey)
    print("Received the server public key")

    # Generating client ID and nonce to send to server
    print("Generating the client ID and nonce 1")
    clientId = b'client ID'
    n1 = b'N1'

    # Send client ID and nonce, encrypted with the server public key
    s.sendall(serverPubKey.encrypt(clientId, padding=True))
    s.sendall(serverPubKey.encrypt(n1, padding=True))
    print("Sent client ID and nonce 1, encrypted with the server public key")

    # Expecting to receive nonce 1 and 2 encrypted with the client public key
    n1_e = s.recv(BUFFER)
    n2_e = s.recv(BUFFER)
    print("Received encrypted messages:")
    print(n1_e)
    print(n2_e)
    n1_e = clientPubKey.decrypt(n1_e, padding=True)
    
    # Ensure that the incoming nonce matches
    if(n1 != n1_e):
        print("Expected nonce 1 from server but received:")
        print(n1_e)
        print("Terminating session...")
        s.close()
        exit()

    n2_e = clientPubKey.decrypt(n2_e, padding=True)
    print("Decrypted messages into:")
    print(n1_e)
    print(n2_e)

    # Send nonce 2 to server
    s.sendall(serverPubKey.encrypt(n2_e, padding=True))

    # Send nonce 1 back to the server, along with the session key
    s.sendall(serverPubKey.encrypt(n1, padding=True))
    s.sendall(serverPubKey.encrypt(Ks, padding=True))

    print(" ")
    print("Established secure channel, start chatting!")
    print("(Type 'q' at any time to quit)")
    startChatSession(s, Ks)