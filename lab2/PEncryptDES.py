from des import DesKey

# Type of key and plaintext must be bytes, not string
# Key must be of length 8, 16, or 24
key = DesKey(b'some key')
userInput = input('Enter your plaintext: ')
plaintext = bytes(userInput, 'utf-8')

# DES requires the message to be of a length that is a multiple of 8,
# setting padding=True tells Python to do the padding for you
ciphertext = key.encrypt(plaintext, padding=True) # ECB Mode is used here
print("The ciphertext is:")
print(ciphertext)

print("The plaintext is:")
print(key.decrypt(ciphertext, padding=True))