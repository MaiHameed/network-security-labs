# Use the Caesar method to cipher plaintext with provided key
def encrypt(plaintext, key):
    ciphertext = "" # Initialize empty string to store result
    # Parses plaintext by character
    for c in plaintext:
        if(ord(c) >= 65 and ord(c) <= 90):
            # Character is uppercase
            ciphertext += chr(((ord(c) - 65 + key) % 26) + 65)
        elif(ord(c) >= 97 and ord(c) <= 122):
            # Character is lowercase
            ciphertext += chr(((ord(c) - 97 + key) % 26) + 97) 
        else:
            # Character is a space or a symbol   
            ciphertext += c 
        
    return ciphertext

print("Welcome to the Caesar Cipher!")
plaintext = input("Please enter your plaintext: ")
print()

print("A Caesar Cipher key is the number of letters that will be shifted")
print("i.e. 3 will turn a -> a+3 = d, b -> e, m -> o etc.")
key = int(input("Please enter your key (integer): "))

print("Plaintext:")
print(plaintext)
print("Ciphertext:")
print(encrypt(plaintext,key))