from datetime import datetime

# Инициализация пустого списка словарей для заметок
notes = []


def add_note():
    """Добавляет новую заметку в список"""
    while True:
        username = input("Введите имя пользователя: ").strip()
        if username:
            break
        print("Имя пользователя не может быть пустым!")

    # Ввод заметок
    contents = []
    print("\nВвод заметок (пустая строка для завершения):")
    while True:
        content = input("Введите заметку: ").strip()
        if content == "":
            break
        contents.append(content)

    # Ввод заголовков
    headers = []
    print("\nВвод заголовков (пустая строка для завершения):")
    while True:
        header = input("Введите заголовок: ").strip()
        if header == "":
            break
        headers.append(header)

    # Ввод даты
    while True:
        date_str = input("Введите дату в формате ДД.ММ.ГГГГ: ")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y")
            break
        except ValueError:
            print("Ошибка: Неверный формат даты")

    # Создание словаря с данными заметки
    note = {
        'username': username,
        'contents': contents,
        'headers': headers,
        'date': date_str,
        'status': 'в процессе'
    }

    notes.append(note)
    print("\nЗаметка успешно добавлена!")


def display_notes():
    """Показывает все заметки"""
    if not notes:
        print("\nСписок заметок пуст!")
        return

    print("\nСписок всех заметок:")
    for i, note in enumerate(notes, 1):
        print(f"\nЗаметка {i}:")
        print(f"Пользователь: {note['username']}")
        print("Содержание:")
        for content in note['contents']:
            print(f"- {content}")
        print("Заголовки:")
        for header in note['headers']:
            print(f"- {header}")
        print(f"Дата: {note['date']}")
        print(f"Статус: {note['status']}")


def main():
    while True:
        print("\nМеню:")
        print("1. Добавить заметку")
        print("2. Показать заметки")
        print("3. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            display_notes()
        elif choice == "3":
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()