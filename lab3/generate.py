import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding 
from cryptography.hazmat.primitives import serialization, hashes
from file_util import ensure_directory

def generate_symmetric_key(key_bits):
    if key_bits < 32 or key_bits > 448:
        raise ValueError("Длина ключа должна быть в пределах допустимого (32 - 448 бита)\n")
    
    if key_bits % 8 != 0:
        raise ValueError("Длина ключа должна быть кратна 8\n")
    
    key_bytes = key_bits // 8
    key = os.urandom(key_bytes)
    
    print(f"Сгенерирован симметричный ключ Blowfish: {key_bits} бит\n")
    return key

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    
    print("Сгенерирована RSA пара ключей: 2048 бит\n")
    return private_key, public_key

def save_private_key(private_key, filepath):
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
    try:
        with open(filepath, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo))
        return True

    except Exception as error:
        print(f"Не удалось сериализовать закрытый ключ в {filepath}: {error}\n")
        return False

def encrypt_symmetric_key(symmetric_key, public_key, filepath):
    try: 
        with open(filepath, 'wb') as key_file:
            encrypt_key = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
            key_file.write(encrypt_key)
        return True

    except Exception as error:
        print(f"Не удалось сериализовать симмтричный ключ в {filepath}: {error}\n")
        return False

def generate(lenght_symmetric_key, symmetric_key_path, public_key_path, private_key_path):
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
