import json
import os
from datetime import datetime

# Функция для очистки экрана
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(file_path, data):
    # Создаем папку js, если её нет
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def manage_items(file_path, item_type):
    while True:
        clear_screen()
        data = load_data(file_path)
        
        print(f"=== Управление: {item_type} ===")
        print(f"Файл: {file_path}\n")
        print("1. Добавить новый элемент")
        print("2. Редактировать существующий")
        print("3. Удалить элемент")
        print("0. Вернуться в главное меню")
        
        cmd = input("\nВыберите действие: ")
        
        if cmd == '0':
            break
            
        if cmd == '1':
            clear_screen()
            print(f"--- Добавление: {item_type} ---")
            if item_type == "Моды":
                new_item = {
                    "name": input("Название: "),
                    "downloadUrl": input("URL: "),
                    "filename": input("Имя файла: "),
                    "isMandatory": input("Обязательный? (y/n): ").lower() == 'y'
                }
            else:
                new_item = {
                    "title": input("Заголовок: "),
                    "date": datetime.now().strftime("%d.%m.%Y"),
                    "text": input("Текст: ")
                }
            data.insert(0, new_item)
            save_data(file_path, data)
            input("\nУспешно добавлено! Нажмите Enter...")

        elif cmd in ['2', '3']:
            if not data:
                input("\nСписок пуст! Нажмите Enter...")
                continue
                
            clear_screen()
            print(f"--- Выберите {item_type} ---")
            for i, item in enumerate(data):
                display_name = item.get('name') or item.get('title')
                print(f"{i}. {display_name}")
            
            try:
                idx = int(input(f"\nВведите номер для {'редактирования' if cmd=='2' else 'удаления'} (или любой другой текст для отмены): "))
                if 0 <= idx < len(data):
                    if cmd == '2':
                        clear_screen()
                        print("Оставьте поле пустым, чтобы сохранить текущее значение.\n")
                        for key in data[idx]:
                            current_val = data[idx][key]
                            new_val = input(f"{key} [{current_val}]: ")
                            if new_val:
                                if key == "isMandatory":
                                    data[idx][key] = new_val.lower() == 'y'
                                else:
                                    data[idx][key] = new_val
                        save_data(file_path, data)
                        input("\nИзменено! Нажмите Enter...")
                    else:
                        confirm = input(f"Удалить '{data[idx].get('name') or data[idx].get('title')}'? (y/n): ")
                        if confirm.lower() == 'y':
                            data.pop(idx)
                            save_data(file_path, data)
                            input("\nУдалено! Нажмите Enter...")
                else:
                    input("\nНеверный номер! Нажмите Enter...")
            except ValueError:
                continue

def main():
    while True:
        clear_screen()
        print("==============================")
        print("    АДМИН-ПАНЕЛЬ ЛАУНЧЕРА     ")
        print("==============================")
        print("1. Моды (js/mods.json)")
        print("2. Новости (js/news.js)")
        print("0. Выход")
        
        choice = input("\nВыбор действия: ")
        
        if choice == '1':
            manage_items('js/mods.json', "Моды")
        elif choice == '2':
            manage_items('js/news.js', "Новости")
        elif choice == '0':
            clear_screen()
            print("Работа завершена.")
            break

if __name__ == "__main__":
    main()