import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def add_padding(text):
    "Добавление паддинга"
    padder = padding.ANSIX923(64).padder()
    padded_text = padder.update(text)+padder.finalize()
    return padded_text

def remove_padding(padded_text):
    "Удаление паддинга"
    if padded_text is None:
        print("Некорректные данные для депаддинга")
        return None
    unpadder = padding.ANSIX923(64).unpadder()
    unpadded_text = unpadder.update(padded_text) + unpadder.finalize()
    return unpadded_text

def blowfish_encrypt(padded_text, key):
    "Шифрование текста + IV вектора инициализации"
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_text) + encryptor.finalize()
    return iv, cipher_text

def blowfish_decrypt(cipher_text, key, iv):
    "Дешифрование текста"
    if cipher_text is None or key is None or iv is None:
        print("Некорректные данные для дешифрования")
        return None
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypt_text = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypt_text

def save_encrypt_text(filepath, iv, cipher_text):
    "Сохранение зашифрованного текста в файл"
    try:
        with open(filepath, 'wb') as enc_file:
            enc_file.write (iv + cipher_text)
            return True

    except Exception as error:
        print(f"Не удалось сохранить зашифрованный текст {filepath}: {error}\n")
        return None

def read_encrypt_text(filepath):
    "Чтение зашифрованного текста из файла"
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
