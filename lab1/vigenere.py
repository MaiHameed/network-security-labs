
def obtainKeyArray(keyPhrase):
    # This method takes a key word and returns the corresponding
    # int array for use in encrypting/decrypting
    keyArray = []
    keyPhrase = keyPhrase.lower()
    for c in keyPhrase:
        keyArray.append(ord(c)-97)
    return keyArray

def letterEncrypt(c, key):
    if(ord(c) >= 65 and ord(c) <= 90):
        # Character is uppercase
        ciphertext = chr(((ord(c) - 65 + key) % 26) + 65)
    elif(ord(c) >= 97 and ord(c) <= 122):
        # Character is lowercase
        ciphertext = chr(((ord(c) - 97 + key) % 26) + 97) 
    else:
        # Character is a space or a symbol   
        ciphertext = c 
        
    return ciphertext

def letterDecrypt(c, key):
    if(ord(c) >= 65 and ord(c) <= 90):
        # Character is uppercase
        ciphertext = chr(((ord(c) - 65 - key) % 26) + 65)
    elif(ord(c) >= 97 and ord(c) <= 122) :
        # Character is lowercase
        ciphertext = chr(((ord(c) - 97 - key) % 26) + 97) 
    else:
        # Character is a space or a symbol   
        ciphertext = c 
        
    return ciphertext

def encrypt(keyPhrase, plainText):
    cipherText = ""
    keyArray = obtainKeyArray(keyPhrase)
    i = 0
    for c in plainText:
        cipherText += letterEncrypt(c, keyArray[i%len(keyArray)])
        i += 1
    return cipherText

def decrypt(keyPhrase, cipherText):
    plainText = ""
    keyArray = obtainKeyArray(keyPhrase)
    i = 0
    for c in cipherText:
        plainText += letterDecrypt(c, keyArray[i%len(keyArray)])
        i += 1
    return plainText

key = "RELATIONS"

cipherText = encrypt(key,"TO BE OR NOT TO BE THAT IS THE QUESTION")
plainText = decrypt(key,cipherText)

print(cipherText)
print(plainText)