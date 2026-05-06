import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding 
from cryptography.hazmat.primitives import serialization, hashes
from file_util import ensure_directory
from asymmetric import encrypt_symmetric_key

def generate_symmetric_key(key_bits):
    "Генерация симметричного ключа"
    if key_bits < 32 or key_bits > 448:
        raise ValueError("Длина ключа должна быть в пределах допустимого (32 - 448 бита)\n")
    
    if key_bits % 8 != 0:
        raise ValueError("Длина ключа должна быть кратна 8\n")
    
    key_bytes = key_bits // 8
    key = os.urandom(key_bytes)
    
    print(f"Сгенерирован симметричный ключ Blowfish: {key_bits} бит\n")
    return key

def generate_rsa_keys():
    "Генерация пары ассиметричных RSA ключей"
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    
    print("Сгенерирована RSA пара ключей: 2048 бит\n")
    return private_key, public_key

def save_private_key(private_key, filepath):
    "Сереализация закрытого ключа"
    try:
        with open(filepath, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()))
        return True

    except Exception as error:
        print(f"Не удалось сериализовать открытый ключ в {filepath}: {error}\n")
        return False

def save_public_key(public_key, filepath):
    "Сереализация открытого ключа"
    try:
        with open(filepath, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo))
        return True

    except Exception as error:
        print(f"Не удалось сериализовать закрытый ключ в {filepath}: {error}\n")
        return False
