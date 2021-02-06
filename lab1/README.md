# COE817-labs

This lab explores simple ciphering. Details can be found in the [lab manual](Lab1_2021.pdf)

## [encrypt.py](encrypt.py)

This script takes a plaintext and a key and encrypts the plaintext using the key and the Caesar Cipher algorithm.
The Caesar algorithm is a simple algorithm that takes the plaintext algorithm ABCD...XYZ and shifts the alphabet left
or right by a certain number of places that is defined by the key. Therefore, each plaintext alphabet character has 
a different alphabet character assigned to it as its encrypted ciphertext alphabet character.

For example, for a key of 3, the plaintext/ciphertext combination would be as follows:
```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 
D E F G H I J K L M N O P Q R S T U V W X Y Z A B C 
```
where an `A` would turn into `D` and so on. So the plaintext `Hello World!` would turn 
into `Khoor Zruog!`

## [decrypt.py](decrypt.py)

This script takes a ciphered message read in from the [secretMessage.txt](secretMessage.txt) file and brute forces the decryption. There are 26 possible keys ranging from 0 to 25, and the script runs the decryption using each key and writes the result to the [decrypted.txt](decrypted.txt) file. Simply open the file and look for the plaintext result written in plain English, which happens to be key 6 in this case.

## [vigenere.py](vigenere.py)

This script uses the Vigenere cipher method to encrypt and decrypt the sample text `TO BE OR NOT TO BE THAT IS THE QUESTION` with the provided key `RELATIONS`. The result is `KS BX CE ESE MW OW XSAM WF KLP JCSFLZSY` The script is modularized and the plaintext and key is modifiable. 
