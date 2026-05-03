import os 

def ensure_directory(filepath):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Создана папка: {directory}\n")
            return True
        except OSError as error:
            print(f"Не удалось создать папку {directory}: {error}\n")
            return False
    return True

def write_text(filepath, text):
    if not ensure_directory(filepath):
        print(f"Директория файла {filepath} не найдена\n")
        return False
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as error:
        print(f"Не удалось записать {filepath}: {error}\n")
        return False

def read_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}\n")
        return None
    except Exception as error:
        print(f"Не удалось прочитать {filepath}: {error}\n")
        return None