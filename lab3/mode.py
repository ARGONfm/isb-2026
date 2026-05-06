import os
import sys
from file_util import ensure_directory, read_text, write_text

from symmetric import (
    add_padding,
    blowfish_encrypt,
    blowfish_decrypt,
    save_encrypt_text,
    read_encrypt_text,
    remove_padding
)

from asymmetric import (
    load_private_key, 
    decrypt_symmetric_key, 
    encrypt_symmetric_key
)

from generate import (
    generate_symmetric_key, 
    generate_rsa_keys, 
    save_private_key, 
    save_public_key
)

def generate(lenght_symmetric_key, symmetric_key_path, public_key_path, private_key_path):
    "Режим генерации ключей"
    print ("Генерация всех ключей:\n")
    
    ensure_directory(symmetric_key_path)
    ensure_directory(public_key_path)
    ensure_directory(private_key_path)

    symmetric_key = generate_symmetric_key(lenght_symmetric_key)
    private_key, public_key = generate_rsa_keys()

    save_private_key(private_key, private_key_path)
    print(f"Закрытый ключ сохранен в {private_key_path}\n")
    save_public_key(public_key, public_key_path)
    print(f"Открытый ключ сохранен в {public_key_path}\n")
    encrypt_symmetric_key(symmetric_key, public_key, symmetric_key_path)
    print(f"Зашифрованный симметричный ключ сохранен в {symmetric_key_path}\n")
    return True

def encrypt (text_path, private_key_path, symmetric_key_path, encrypt_text_path):
    "Режим шифрования текста"
    print ("Шифрование данных:\n")

    private_key = load_private_key(private_key_path)
    symmetric_key = decrypt_symmetric_key(symmetric_key_path, private_key)

    text = read_text(text_path)
    text_bytes = text.encode('utf-8')
    padded_text = add_padding(text_bytes)

    iv, cipher_text = blowfish_encrypt(padded_text, symmetric_key)
    ensure_directory(encrypt_text_path)
    save_encrypt_text(encrypt_text_path, iv, cipher_text)

    print(f"Зашифрованный текст сохранен в {encrypt_text_path} \n")
    return True

def decrypt(encrypt_text_path, private_key_path, symmetric_key_path, text_path):
        "Режим дешифрования текста"
        print ("Дешифрование данных:\n")

        private_key = load_private_key(private_key_path)
        symmetric_key = decrypt_symmetric_key(symmetric_key_path, private_key)

        iv, cipher_text = read_encrypt_text(encrypt_text_path)
        padded_text = blowfish_decrypt(cipher_text, symmetric_key, iv)
        text_bytes = remove_padding(padded_text)
        text = text_bytes.decode('utf-8')
        ensure_directory(text_path)
        write_text(text_path, text)

        print(f"Расшифрованный текст сохранён в {text_path} \n")
        return True
