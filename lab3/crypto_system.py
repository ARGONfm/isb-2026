import argparse
import json
import sys

def load_settings(settings_path):
    """Загружает настройки из JSON-файла"""
    try:
        with open(settings_path, 'r', encoding='utf-8') as json_file:
            settings = json.load(json_file)
        print(f"Загружены настройки: {settings_path}\n")
        return settings
    except FileNotFoundError:
        print(f"Ошибка: файл настроек {settings_path} не найден\n")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка: неверный формат JSON: {e}\n")
        sys.exit(1)

def main ():
    parser = argparse.ArgumentParser (description="Гибридная криптосистема:" )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen','--generate', action='store_true',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encrypt', action='store_true',help='Запускает режим шифрования')
    group.add_argument('-dec','--decrypt', action='store_true',help='Запускает режим дешифрования')

    parser.add_argument('--keylen', type=int, default=128, help='Длина ключа от 32 до 448 бит с шагом 8 бит')
    parser.add_argument('--sym-out', default='keys/symmetric_encrypted.bin', help='Путь для зашифрованного симметричного ключа')
    parser.add_argument('--pub-out', default='keys/public.pem', help='Путь для открытого RSA-ключа')
    parser.add_argument('--priv-out', default='keys/private.pem', help='Путь для закрытого RSA-ключа')

    parser.add_argument('--input', help='Путь к входному файлу')
    parser.add_argument('--output', help='Путь к выходному файлу')
    parser.add_argument('--priv-key', help='Путь к закрытому RSA-ключу (private.pem)')
    parser.add_argument('--sym-key', help='Путь к зашифрованному симметричному ключу')

    parser.add_argument('--settings', default='settings.json', help='Путь к файлу настроек')
    
    args = parser.parse_args()

    settings = load_settings(args.settings)

    match args:
        case _ if args.generate:
            print("___Генерация ключей гибридной системы___")
            generate(
                lenght_symmetric_key=args.keylen,
                symmetric_key_path=args.sym_out,
                public_key_path=args.pub_out,
                private_key_path=args.priv_out
            )
        
        case _ if args.encrypt:
            print("___Шифрование данных гибридной системой___")
            encrypt(
                text_path=args.input or settings['initial_file'],
                private_key_path=args.priv_key or settings['secret_key'],
                symmetric_key_path=args.sym_key or settings['symmetric_key'],
                encrypt_text_path=args.output or settings['encrypted_file']
            )
        
        case _ if args.decrypt:
            print("___Дешифрование данных гибридной системой___")
            decrypt(
                encrypt_text_path=args.input or settings['encrypted_file'],
                private_key_path=args.priv_key or settings['secret_key'],
                symmetric_key_path=args.sym_key or settings['symmetric_key'],
                text_path=args.output or settings['decrypted_file']
            )
        
        case _:
            print("Ошибка: неизвестный режим работы")
            sys.exit(1)

if __name__ == "__main__":
    main ()
