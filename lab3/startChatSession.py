from des import DesKey
from PIL import Image
from io import BytesIO
import select
import socket
import sys
import os

BUFFER = 1024

# conn (socket) is the socket that connects the current user to the end user
# Ks (bytes) is the plaintext of the 8, 16, or 24bit DES key
# chatTo (string) who the end user that the current user is chatting with [client|server]
def startChatSession(conn, Ks, chatTo):
    # Determine who the current user is, required to access image repo
    if(chatTo == 'server'):
        user = 'client'
    else:
        user = 'server'

    print(" ")
    print("Established secure channel, start chatting!")
    print("(Type 'i' to send an image from your image repository '"+user+"ImageRepo'")
    print("(Type 'q' at any time to quit)")

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
                
                # Check if current user wants to quit
                if(message == 'q'):
                    print("Terminating chat session")
                    conn.close()
                    exit()
                
                # Check if current user wants to send an image
                if(message == 'i'):
                    # List all available images in the repo
                    print("Your image repo contains the following images:")
                    imageRepoPath = "./"+user+"ImageRepo" 
                    x = 0
                    for img in os.listdir(imageRepoPath):
                        print(str(x)+": "+img)
                        x = x+1
                    
                    # Prompt user for an image selection
                    imgSelection = input("Select an image by typing the associated number: ")
                    x = 0
                    # TODO: Potentially implement error catching if current user submits a wrong input.
                    #       Implement if I have time later
                    # Send image to end user
                    for img in os.listdir(imageRepoPath):
                        if (int(imgSelection) == x):
                            imgFilename = os.listdir(imageRepoPath)[x]
                            imgObj = Image.open(imageRepoPath+"/"+imgFilename)

                            print("Sending "+imgFilename+" to "+chatTo+"...")
                            
                            # Initial flag to specify incoming message type to end user
                            conn.sendall(b'I')
                            imgEncrypted = Ks.encrypt(imgObj.tobytes(), padding=True)
                            # Send size of message to end user
                            sizeOfMessage = len(imgEncrypted)
                            conn.sendall(sizeOfMessage.to_bytes(8,'big'))
                            # Send image data
                            bytesRemaining = sizeOfMessage
                            while(1):
                                if(bytesRemaining > BUFFER):
                                    conn.sendall(imgEncrypted[:BUFFER],BUFFER)
                                    imgEncrypted = imgEncrypted[BUFFER:]
                                    bytesRemaining = bytesRemaining - BUFFER
                                else:
                                    conn.sendall(imgEncrypted,bytesRemaining)
                                    break
                            print("Image sent successfully!")
                            break
                        x = x+1  
                else: 
                    # Encrypt and send message to end user
                    message = bytes(message,'utf-8')
                    message = Ks.encrypt(message, padding=True)
                    # Initial flag to specify incoming message type to end user
                    conn.sendall(b'T')
                    conn.sendall(message)
            
            # Message from end user
            else:
                try:
                    # Receive message flag T for text I for image
                    receivedMessage = conn.recv(1)
                except:
                    print("Chat session terminated by "+chatTo)
                    conn.close()
                    exit()

                # Terminate chat session if end user terminated
                if (not receivedMessage):
                    print("Chat session terminated by "+chatTo)
                    conn.close()
                    exit()
                
                if(receivedMessage == b'T'):
                    # Get actual message
                    receivedMessage = conn.recv(BUFFER)
                    # .capitalize() just capitalizes the first letter of the string
                    print(chatTo.capitalize()+" Encrypted: "+str(receivedMessage))
                    receivedMessage = Ks.decrypt(receivedMessage, padding=True)
                    print(chatTo.capitalize()+" Decrypted: "+str(receivedMessage,'utf-8'))
                elif(receivedMessage == b'I'):
                    print(chatTo.capitalize()+" wants to send an image")
                    print("Downloading image...")
                    # Get image size information from end user
                    messageSize = int.from_bytes(conn.recv(8),'big')
                    print("Incoming image size in bytes is: "+str(messageSize))
                    bytesRemaining = messageSize
                    image = b''
                    while(1):
                        if(bytesRemaining > BUFFER):
                            image = image + conn.recv(BUFFER)
                            bytesRemaining = bytesRemaining - BUFFER
                        else:
                            image = image + conn.recv(bytesRemaining)
                            break
                    print("Image data not displayed due to it's length")
                    # The decrypted image data
                    print("Decrypting image...")
                    imageRawBytes = Ks.decrypt(image, padding=True)
                    # TODO: Remove the constraint on image size if I have time
                    image = Image.frombytes("RGB", (100,100), imageRawBytes)
                    
                    # Save image to local repository
                    downloadedFilePath = "./"+user+"ImageRepo/download.jpg"
                    image.save(downloadedFilePath)
                    print("Download complete! View image at "+downloadedFilePath)
                    image.show()