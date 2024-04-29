import random
import string
from tabulate import tabulate

# Function to generate a random key of the same length as the plaintext
def generate_random_key(plaintext):
    key = ''.join(random.choice(string.ascii_letters) for _ in plaintext)
    return key

# Function to perform XOR operation on two binary strings
def binary_xor(bin1, bin2):
    result = ""
    for i in range(8):
        result += '1' if bin1[i] != bin2[i] else '0'
    return result

# Function to convert a character to binary and pad with 0s
def char_to_binary(char):
    binary = bin(ord(char))[2:]
    return binary.zfill(8)  # Pad with 0s to make it 8 bits long

# Encryption function
def encrypt(plaintext, key):
    encryption_steps = []
    encrypted_text = ""
    for i in range(len(plaintext)):
        binary_plain = char_to_binary(plaintext[i])
        binary_key = char_to_binary(key[i % len(key)])
        result_binary = binary_xor(binary_plain, binary_key)
        hex_value = hex(int(
            result_binary, 2)
            )[2:].zfill(2)
        encryption_steps.append([plaintext[i], 
                                 ord(plaintext[i]), 
                                 binary_plain, 
                                 binary_key, 
                                 result_binary, 
                                 hex_value])
        encrypted_text += hex_value

    return encrypted_text, encryption_steps

# Decryption function
def decrypt(encrypted_text, key):
    decryption_steps = []
    decrypted_text = ""
    for i in range(0, len(encrypted_text), 2):
        hex_value = encrypted_text[i:i+2]
        binary_plain = bin(int(hex_value, 16))[2:].zfill(8)
        binary_key = char_to_binary(key[i // 2 % len(key)])
        result_binary = binary_xor(binary_plain, binary_key)
        char = chr(int(result_binary, 2))
        decryption_steps.append([hex_value, 
                                 binary_plain, 
                                 binary_key, 
                                 result_binary, 
                                 char, 
                                 ord(char)])
        decrypted_text += char

    return decrypted_text, decryption_steps

# Handle user input errors
def get_valid_input(prompt, error_message):
    while True:
        user_input = input(prompt)
        if user_input:
            return user_input
        else:
            print(error_message)

# Ask for encryption or decryption as the first input
option = get_valid_input("Select an option:\n1. Encrypt\n2. Decrypt\nEnter 1 or 2: ", 
                         "Error: Please enter 1 for encryption or 2 for decryption.")

if option == "1":
    # Input plaintext
    plaintext = get_valid_input("Enter plaintext: ", 
                                "Error: Please provide plaintext.")
    
    # Ask the user for a key or generate a random key if none provided
    key = input("Enter key (press Enter for random key): ")
    if not key:
        key = generate_random_key(plaintext)
    else:
        # Ensure the key is the same length as the plaintext
        key = key[:len(plaintext)]

    # Encrypt the plaintext
    encrypted_text, encryption_steps = encrypt(plaintext, key)
    encryption_table = tabulate(encryption_steps, 
                                headers=["Character",
                                         "ASCII", 
                                         "Binary Plain", 
                                         "Binary Key", 
                                         "XOR Result", 
                                         "Hex"], 
                                tablefmt="pretty")
    print("\nKey: ", key)
    print("Encryption Steps:")
    print(encryption_table)
    print("Encrypted Text: ", encrypted_text)

elif option == "2":
    key = get_valid_input("Enter the decryption key: ", 
                          "Error: Please provide the decryption key.")
    encrypted_text = get_valid_input("Enter the encrypted text: ", 
                                     "Error: Please provide the encrypted text.")

    # Decrypt the encrypted text
    decrypted_text, decryption_steps = decrypt(encrypted_text, key)
    decryption_table = tabulate(decryption_steps, 
                                headers=["Hex Value", 
                                         "Binary Plain", 
                                         "Binary Key", 
                                         "XOR Result", 
                                         "Character", 
                                         "ASCII"], 
                                tablefmt="pretty")
    print("\nDecryption Key: ", key)
    print("Decryption Steps:")
    print(decryption_table)
    print("Decrypted Text: ", decrypted_text)