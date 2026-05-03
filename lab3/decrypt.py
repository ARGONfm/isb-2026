import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from encrypt import load_private_key, load_symmetric_key
from file_util import ensure_directory, write_text

def read_encrypt_text(filepath):
    try:
        with open(filepath, 'rb') as enc_file:
            data = enc_file.read()

        if len(data) < 8:
            print(f"Файл {filepath} не должен быть меньше 8 байт")
            return None, None

        iv = data[:8]
        cipher_text = data[8:]
        return iv, cipher_text
    
    except Exception as error:
        print(f"Не удалось загрузить зашифрованный текст {filepath}: {error}\n")
        return None, None

def blowfish_decrypt(cipher_text, key, iv):
    if cipher_text is None or key is None or iv is None:
        print("Некорректные данные для дешифрования")
        return None
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypt_text = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypt_text

def remove_padding(padded_text):
    if padded_text is None:
        print("Некорректные данные для депаддинга")
        return None
    unpadder = padding.ANSIX923(64).unpadder()
    unpadded_text = unpadder.update(padded_text) + unpadder.finalize()
    return unpadded_text

def decrypt(encrypt_text_path, private_key_path, symmetric_key_path, text_path):
        print ("Дешифрование данных:\n")

        private_key = load_private_key(private_key_path)
        symmetric_key = load_symmetric_key(symmetric_key_path, private_key)

        iv, cipher_text = read_encrypt_text(encrypt_text_path)
        padded_text = blowfish_decrypt(cipher_text, symmetric_key, iv)
        text_bytes = remove_padding(padded_text)
        text = text_bytes.decode('utf-8')
        ensure_directory(text_path)
        write_text(text_path, text)

        print(f"Расшифрованный текст сохранён в {text_path} \n")
        return True
