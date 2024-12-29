from datetime import datetime

# Инициализация переменных
titles = []
used_titles = set()

# Словарь для хранения статусов заметок
note_statuses = {
    1: "выполнено",
    2: "в процессе",
    3: "отложено"
}

def display_current_status(current_status):
    """Отображает текущий статус заметки"""
    print(f"\nТекущий статус заметки: \"{current_status}\"")

def show_status_options():
    """Показывает список доступных статусов"""
    print("\nВыберите новый статус заметки:")
    for key, value in note_statuses.items():
        print(f"{key}. {value}")

def get_user_choice():
    """Получает и проверяет выбор пользователя"""
    while True:
        try:
            choice = int(input("\nВаш выбор: "))
            if choice in note_statuses:
                return choice
            else:
                print("Ошибка: Выберите число от 1 до 3")
        except ValueError:
            print("Ошибка: Введите числовое значение")

def update_note_status():
    """Основная функция обновления статуса заметки"""
    current_status = "в процессе"
    display_current_status(current_status)
    show_status_options()
    choice = get_user_choice()
    new_status = note_statuses[choice]
    print(f"\nСтатус заметки успешно обновлён на: \"{new_status}\"")
    return new_status

# Создаем словарь для заметки
note = {}

# Собираем данные
note['username'] = input("Введите имя пользователя: ")
note['content'] = input("Введите содержание заметки: ")
note['status'] = update_note_status()
note['creation_date'] = input("Введите дату заметки в формате ДД.ММ.ГГГГ: ")

# Проверка даты
try:
    issue_date = datetime.strptime(note['creation_date'], "%d.%m.%Y")
    current_date = datetime.now()
    if current_date.date() == current_date.date():
        print("\nПРЕДУПРЕЖДЕНИЕ: Срок выполнения заметки истекает!")
    if current_date.date() > issue_date.date():
        print("\nПРЕДУПРЕЖДЕНИЕ: Срок выполнения заметки истек!")
        print(f"Дата создания: {note['creation_date']}")
        print(f"Текущая дата: {current_date.strftime('%d.%m.%Y')}")
except ValueError:
    print("Ошибка: Неверный формат даты")

# Сбор заголовков
headers = []
while True:
    header = input("Введите заголовок (или Enter для завершения): ")
    if header == "":
        break
    headers.append(header)

note['headers'] = headers

# Вывод информации о заметке
print("\nИнформация о заметке:")
print(f"Имя пользователя: {note['username']}")
print(f"Содержание: {note['content']}")
print(f"Статус: {note['status']}")
print(f"Дата создания: {note['creation_date']}")
print("Заголовки:")
if note['headers']:
    for header in note['headers']:
        print(f"- {header}")