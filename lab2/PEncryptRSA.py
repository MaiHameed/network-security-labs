import rsa

# 512 is the key size in bits
(pubKey, privKey) = rsa.newkeys(512)
userInput = input('Enter your plaintext: ')
plaintext = bytes(userInput, 'utf-8')

# Encryption using the public key 
ciphertext = rsa.encrypt(plaintext, pubKey)
print("The ciphertext is:")
print(ciphertext)

# Decryption using the private key
print("The plaintext is:")
print(rsa.decrypt(ciphertext, privKey))