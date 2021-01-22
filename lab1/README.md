# COE817-labs

This repository includes 2 Python scripts.

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