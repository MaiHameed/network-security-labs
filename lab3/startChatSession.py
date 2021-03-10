from des import DesKey
import select
import socket
import sys

BUFFER = 1024

# conn (socket) is the socket that connects the user to the target
# Ks (bytes) is the plaintext of the 8, 16, or 24bit DES key
# chatTo (string) who the target that the current user is chatting with [client|server]
def startChatSession(conn, Ks, chatTo):
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
                
                # Encrypt and send message to target
                message = bytes(message,'utf-8')
                message = Ks.encrypt(message, padding=True)
                conn.sendall(message)
            
            # Message from target
            else:
                try:
                    receivedMessage = conn.recv(BUFFER)
                except:
                    print("Chat session terminated by "+chatTo)
                    conn.close()
                    exit()

                # Terminate chat session if target terminated
                if (not receivedMessage):
                    print("Chat session terminated by "+chatTo)
                    conn.close()
                    exit()
                
                # .capitalize() just capitalizes the first letter of the string
                print(chatTo.capitalize()+" Encrypted: "+str(receivedMessage))
                receivedMessage = Ks.decrypt(receivedMessage, padding=True)
                print(chatTo.capitalize()+" Decrypted: "+str(receivedMessage,'utf-8'))