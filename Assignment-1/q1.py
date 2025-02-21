from Crypto import Random
import gmpy2 as gm
from Crypto.Cipher import Salsa20 as sal

"""
PART A
"""
key = Random.get_random_bytes(16)
key_in_int = int(key.hex(),base=16)
print("Generated Key in bytes is: ",key)
print("Key in Int is: ",key_in_int)

"""
PART B
"""

print("Enter the prime numbers: p and q for part b:-----")
PRIME_NUMBER_P = input("Enter the value of p: ")
PRIME_NUMBER_Q = input("Enter the value of q: ")

PRIME_NUMBER_P = gm.mpz(PRIME_NUMBER_P)
PRIME_NUMBER_Q = gm.mpz(PRIME_NUMBER_Q)

N = PRIME_NUMBER_P * PRIME_NUMBER_Q
EULER_TOIENT_FUNC = (PRIME_NUMBER_P-1)*(PRIME_NUMBER_Q-1)
PUBLIC_EXPONENT = 65537
D = gm.invert(PUBLIC_EXPONENT, EULER_TOIENT_FUNC)


print("\nPublic Key is:--")
print("N: ",N)
print("E: ",PUBLIC_EXPONENT)


print("\nPrivate Key is:--")
print("N: ",N)
print("D: ",D)


"""
PART C
"""

#NUMBER_RAISED_TO_EXPONENT = key_in_int ** PUBLIC_EXPONENT
# = (NUMBER_RAISED_TO_EXPONENT % N)
CIPHERTEXT=gm.powmod(key_in_int, PUBLIC_EXPONENT, N)
print("The CypherText is:---")
print(CIPHERTEXT)


"""
PART D 
"""

ORIGINAL_MSG=gm.powmod(CIPHERTEXT, D, N)
print("\nThe original message (Key in this case) is:--")
print(f"\nKey in Int: {ORIGINAL_MSG}")

KEY_IN_HEX = hex(ORIGINAL_MSG)[2:] 
KEY_IN_BYTES = bytes.fromhex(KEY_IN_HEX)
print(f"\nKey in Bytes: {KEY_IN_BYTES}")



"""
PART E
"""

BOB_MSG = b"THIS IS A MESSAGE FROM BOB TO ALICE WHICH USED SHARED SYMMETRIC KEY"
CIPHER = sal.new(key=KEY_IN_BYTES)
RANDOM_NONCE = CIPHER.nonce
ENCRYPTED_MSG = CIPHER.encrypt(BOB_MSG)
print("Original Message without encryption is: ",BOB_MSG.decode())
print("The Encrypted Message from bob is: ",ENCRYPTED_MSG)



"""
PART F
"""

SHARED_KEY = KEY_IN_BYTES
ALICE_SALSA = sal.new(key=SHARED_KEY,nonce=RANDOM_NONCE)
DECRYPTED_MSG = ALICE_SALSA.decrypt(ENCRYPTED_MSG)

print("The Decrypted Message at Alice's End is: ",DECRYPTED_MSG.decode())