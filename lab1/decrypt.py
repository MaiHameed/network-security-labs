inFile = open("secretMessage.txt", "r")
ciphertext = inFile.read()
inFile.close()

outFile = open("decrypted.txt", "w")

def decrypt(key):
    plaintext = ""
    for c in ciphertext:
        if(ord(c) >= 65 and ord(c) <= 90):
            # Character is uppercase
            plaintext += chr(((ord(c) - 65 - key) % 26) + 65)
        elif(ord(c) >= 97 and ord(c) <= 122):
            # Character is lowercase
            plaintext += chr(((ord(c) - 97 - key) % 26) + 97)
        else:
            # Character is a space or a symbol  
            plaintext += c 
    return plaintext

# Brute Force through all 26 keys
for key in range(26):
    outFile.write("Key: "+str(key)+"\n")
    outFile.write(decrypt(key)+"\n")

outFile.close()