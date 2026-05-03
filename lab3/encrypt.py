import os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from file_util import ensure_directory, read_text

def load_private_key(filepath):
    try:
        with open (filepath, 'rb') as pem_in:
            private_bytes = pem_in.read()
            private_key = load_pem_private_key(private_bytes,password=None,)
            print (f"Десериализован закрытый ключ из {filepath} \n")
            return private_key

    except Exception as error:
        print(f"Не удалось десериализовать закрытый ключ {filepath}: {error}\n")
        return None

def load_symmetric_key (filepath, private_key):
    try:
        with open (filepath, mode='rb') as key_file:
            symmetric_bytes = key_file.read()
            symmetric_key = private_key.decrypt(symmetric_bytes,asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
            print (f"Десериализован симметричный ключ из {filepath} \n")
            return symmetric_key

    except Exception as error:
        print(f"Не удалось десериализовать симметричный ключ {filepath}: {error}\n")
        return None

def add_padding(text):
    padder = padding.ANSIX923(64).padder()
    padded_text = padder.update(text)+padder.finalize()
    return padded_text

def blowfish(padded_text, key):
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_text) + encryptor.finalize()
    return iv, cipher_text

def save_encrypt_text(filepath, iv, cipher_text):
    try:
        with open(filepath, 'wb') as enc_file:
            enc_file.write (iv + cipher_text)
            return True

    except Exception as error:
        print(f"Не удалось сохранить зашифрованный текст {filepath}: {error}\n")
        return None

def encrypt (text_path, private_key_path, symmetric_key_path, encrypt_text_path):
    print ("Шифрование данных:\n")

    private_key = load_private_key(private_key_path)
    symmetric_key = load_symmetric_key(symmetric_key_path, private_key)

    text = read_text(text_path)
    text_bytes = text.encode('utf-8')
    padded_text = add_padding(text_bytes)

    iv, cipher_text = blowfish(padded_text, symmetric_key)
    ensure_directory(encrypt_text_path)
    save_encrypt_text(encrypt_text_path, iv, cipher_text)

    print(f"Зашифрованный текст сохранен в {encrypt_text_path} \n")
    return True