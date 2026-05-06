import os 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def load_private_key(filepath):
    "Загрузка закрытого ключа из файла"
    try:
        with open (filepath, 'rb') as pem_in:
            private_bytes = pem_in.read()
            private_key = load_pem_private_key(private_bytes,password=None,)
            print (f"Десериализован закрытый ключ из {filepath} \n")
            return private_key

    except Exception as error:
        print(f"Не удалось десериализовать закрытый ключ {filepath}: {error}\n")
        return None

def encrypt_symmetric_key(symmetric_key, public_key, filepath):
    "Шифрование симметричного ключа"
    try: 
        with open(filepath, 'wb') as key_file:
            encrypt_key = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
            key_file.write(encrypt_key)
        return True

    except Exception as error:
        print(f"Не удалось сериализовать симмтричный ключ в {filepath}: {error}\n")
        return False

def decrypt_symmetric_key (filepath, private_key):
    "Дешифрование симметричного ключа"
    try:
        with open (filepath, mode='rb') as key_file:
            symmetric_bytes = key_file.read()
            symmetric_key = private_key.decrypt(symmetric_bytes,asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
            print (f"Десериализован симметричный ключ из {filepath} \n")
            return symmetric_key

    except Exception as error:
        print(f"Не удалось десериализовать симметричный ключ {filepath}: {error}\n")
        return None
