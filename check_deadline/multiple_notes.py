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


def validate_date(date_str):
    """Проверяет корректность даты"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None


# Создаем словарь для заметки
note = {}

# Собираем данные
while True:
    username = input("Введите имя пользователя: ").strip()
    if username:
        note['username'] = username
        break
    print("Имя пользователя не может быть пустым!")
# Инициализация списков и множеств
contents = []  # Список для хранения заметок
used_contents = set()  # Множество для проверки дубликатов

# Ввод заметок
print("\nВвод заметок (пустая строка для завершения):")
while True:
    content = input("Введите заметку: ").strip()
    if content == "":
        break
    if content not in used_contents:
        contents.append(content)  # Добавляем в список заметок
        used_contents.add(content)  # Добавляем в множество использованных заметок
    else:
        print("Эта заметка уже существует!")

note['status'] = update_note_status()

while True:
    date_str = input("Введите дату дедлайна в формате ДД.ММ.ГГГГ: ")
    deadline_date = validate_date(date_str)
    if deadline_date:
        note['deadline_date'] = date_str
        current_date = datetime.now()
        time_left = deadline_date - current_date

        # Проверка даты
        if deadline_date.date() == current_date.date():
            print("\nПРЕДУПРЕЖДЕНИЕ: Дедлайн истекает сегодня!")
        elif deadline_date.date() > current_date.date():
            days_left = time_left.days
            if days_left == 1:
                print(f"\nДо дедлайна остался {days_left} день")
            elif 2 <= days_left <= 4:
                print(f"\nДо дедлайна осталось {days_left} дня")
            else:
                print(f"\nДо дедлайна осталось {days_left} дней")
        else:
            days_overdue = abs(time_left.days)
            if days_overdue == 1:
                print("\nПРЕДУПРЕЖДЕНИЕ: Дедлайн просрочен на 1 день!")
            elif 2 <= days_overdue <= 4:
                print(f"\nПРЕДУПРЕЖДЕНИЕ: Дедлайн просрочен на {days_overdue} дня!")
            else:
                print(f"\nПРЕДУПРЕЖДЕНИЕ: Дедлайн просрочен на {days_overdue} дней!")
            print(f"Дата дедлайна: {note['deadline_date']}")
            print(f"Текущая дата: {current_date.strftime('%d.%m.%Y')}")
        break
    print("Ошибка: Неверный формат даты. Используйте формат ДД.ММ.ГГГГ")

# Сбор заголовков
headers = []
print("\nВвод заголовков (пустая строка для завершения):")
while True:
    header = input("Введите заголовок: ").strip()
    if header == "":
        break
    if header not in used_titles:
        headers.append(header)
        used_titles.add(header)
    else:
        print("Этот заголовок уже существует!")

note['headers'] = headers

if contents:
    print("\nВсе введенные заметки:")
    for i, content in enumerate(contents, 1):
        print(f"{i}. {content}")
else:
    print("\nСписок заметок пуст!")
print(f"Имя пользователя: {note['username']}")
print(f"Статус: {note['status']}")
print(f"Дата создания: {note['deadline_date']}")
print("Заголовки:")
if note['headers']:
    for header in note['headers']:
        print(f"- {header}")
else:
    print("Заголовки не добавлены")