import streamlit as st
import hashlib


# Caesar Cipher Functions
def caesar_encrypt(text, shift):
    encrypted = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted += char
    return encrypted


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# Vigenere Cipher Functions
def vigenere_encrypt(text, key):
    encrypted = ""
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_as_int = [ord(i) for i in text]
    for i in range(len(text_as_int)):
        if text[i].isalpha():
            shift_base = ord('A') if text[i].isupper() else ord('a')
            encrypted += chr((text_as_int[i] - shift_base + key_as_int[i % key_length] - shift_base) % 26 + shift_base)
        else:
            encrypted += text[i]
    return encrypted


def vigenere_decrypt(text, key):
    decrypted = ""
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_as_int = [ord(i) for i in text]
    for i in range(len(text_as_int)):
        if text[i].isalpha():
            shift_base = ord('A') if text[i].isupper() else ord('a')
            decrypted += chr(
                (text_as_int[i] - shift_base - (key_as_int[i % key_length] - shift_base)) % 26 + shift_base)
        else:
            decrypted += text[i]
    return decrypted


# Transposition Cipher Functions
def transposition_encrypt(text):
    even_chars = text[::2]
    odd_chars = text[1::2]
    return even_chars + odd_chars


def transposition_decrypt(text):
    # Calculate the midpoint to split the text into even and odd characters
    half_len = (len(text) + 1) // 2
    even_chars = text[:half_len]
    odd_chars = text[half_len:]

    decrypted = []
    for i in range(half_len):
        decrypted.append(even_chars[i])
        if i < len(odd_chars):  # add the odd character if it exists
            decrypted.append(odd_chars[i])
    return ''.join(decrypted)


# Hashing Cipher Function
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


# Streamlit App
st.title("Text Encryption & Decryption")

# Input Text
st.subheader("Enter text:")
text = st.text_area("Text to Encrypt/Decrypt")

# Encryption Method Selection
st.subheader("Select encryption method:")
cipher_method = st.selectbox("Choose a cipher method",
                             ["Caesar Cipher", "Vigenere Cipher", "Transposition Cipher", "Hashing (SHA-256)"])

# Key or Shift Input
if cipher_method not in ["Transposition Cipher", "Hashing (SHA-256)"]:
    st.subheader("Enter shift (Caesar) or key (Vigenere):")
    shift_key = st.text_input("Shift (for Caesar) or Key (for Vigenere)")

# Encrypt or Decrypt Selection
if cipher_method != "Hashing (SHA-256)":
    action = st.radio("Choose action:", ["Encrypt", "Decrypt"])

# Display the Output
if st.button("Execute"):
    # Check inputs
    if not text:
        st.warning("Please enter text to encrypt or decrypt.")
    elif cipher_method == "Caesar Cipher":
        try:
            shift = int(shift_key)
            if action == "Encrypt":
                result = caesar_encrypt(text, shift)
            else:
                result = caesar_decrypt(text, shift)
            st.subheader("Output:")
            st.write(result)
        except ValueError:
            st.warning("Please enter a valid integer for Caesar Cipher shift.")
    elif cipher_method == "Vigenere Cipher":
        key = shift_key
        if not key.isalpha():
            st.warning("Vigenère Cipher key should be alphabetic.")
        else:
            if action == "Encrypt":
                result = vigenere_encrypt(text, key)
            else:
                result = vigenere_decrypt(text, key)
            st.subheader("Output:")
            st.write(result)
    elif cipher_method == "Transposition Cipher":
        if action == "Encrypt":
            result = transposition_encrypt(text)
        else:
            result = transposition_decrypt(text)
        st.subheader("Output:")
        st.write(result)
    elif cipher_method == "Hashing (SHA-256)":
        result = hash_text(text)
        st.subheader("Output (Hash):")
        st.write(result)