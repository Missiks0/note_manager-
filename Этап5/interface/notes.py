from data.note import *
from data.note_manager import *
from utils.enums import Enum
from typing import Any, Callable, Dict, List
from datetime import *
from utils.helpers import *

def update_note_status():
    """Обновляет статус заметки"""
    note_statuses = {
        1: "выполнено",
        2: "в процессе",
        3: "отложено"
    }

    print("\nВыберите статус заметки:")
    for key, value in note_statuses.items():
        print(f"{key}. {value}")

    while True:
        try:
            choice = int(input("\nВаш выбор: "))
            if choice in note_statuses:
                return note_statuses[choice]
            print("Ошибка: Выберите число от 1 до 3")
        except ValueError:
            print("Ошибка: Введите числовое значение")

def display_note(note: Note):
    """Отображает информацию о заметке"""
    print("\n" + "=" * 50)
    print(f"ID: {note.id}")
    print(f"Имя пользователя: {note.username}")
    print(f"Статус: {note.status}")
    print(f"Дата создания: {note.creation_date}")
    print(f"Дата дедлайна: {note.deadline_date}")

    print("\nЗаметки:")
    if note.contents:
        for i, content in enumerate(note.contents, 1):
            print(f"{i}. {content}")
    else:
        print("Список заметок пуст!")

    print("\nЗаголовки:")
    if note.headers:
        for header in note.headers:
            print(f"- {header}")
    else:
        print("Заголовки не добавлены")
    print("=" * 50)

def display_all_notes(note_manager: NoteManager):
    """Отображает все существующие заметки"""
    notes = note_manager.get_all_notes()
    if not notes:
        print("\nСписок заметок пуст")
        return

    print("\nВсе существующие заметки:")
    for i, note in enumerate(notes, 1):
        print(f"\nЗаметка {i}:")
        display_note(note)

def create_note():
    """Создает новую заметку"""
    note = Note()

    # Ввод имени пользователя
    while True:
        username = input("Введите имя пользователя: ").strip()
        if username:
            note.username = username
            break
        print("Имя пользователя не может быть пустым!")

    # Ввод заметок
    print("\nВвод заметок (пустая строка для завершения):")
    while True:
        content = input("Введите заметку: ").strip()
        if content == "":
            break
        if content not in note.contents:
            note.contents.append(content)
        else:
            print("Эта заметка уже существует!")

    # Обновление статуса
    note.status = update_note_status()

    def validate_date(date_str):
        """Проверяет корректность даты"""
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            return None
    # Ввод дат
    while True:
        date_str = input("Введите дату создания в формате ДД.ММ.ГГГГ: ")
        creation_date = validate_date(date_str)
        # Удаляем эту строку, так как validate_date уже проверяет формат
        # datetime.strptime(date_str, "%Y-%m-%d")
        if creation_date:
            note.creation_date = date_str
            break
        print("Ошибка: Неверный формат даты")

    while True:
        date_str = input("Введите дату дедлайна в формате ДД.ММ.ГГГГ: ")
        deadline_date = validate_date(date_str)
        # Удаляем эту строку, так как validate_date уже проверяет формат
        # datetime.datetime.strptime(date_str, "%Y-%m-%d")
        if deadline_date:
            note.deadline_date = date_str
            current_date = datetime.now()
            time_left = deadline_date - current_date

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
            break
        print("Ошибка: Неверный формат даты")

    # Ввод заголовков
    print("\nВвод заголовков (пустая строка для завершения):")
    while True:
        header = input("Введите заголовок: ").strip()
        if header == "":
            break
        if header not in note.headers:
            note.headers.append(header)
        else:
            print("Этот заголовок уже существует!")

    return note

def handle_deletion(note_manager: NoteManager) -> None:
        """Обработка удаления заметок"""
        print("\nВыберите тип удаления:")
        print("1. Удалить по имени пользователя")
        print("2. Удалить по заголовку")
        print("3. Вернуться назад")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            username = input("\nВведите имя пользователя: ").strip()
            if note_manager.delete_by_username(username):
                print(f"\nЗаметки пользователя '{username}' успешно удалены")
            else:
                print(f"\nЗаметки пользователя '{username}' не найдены")

        elif choice == "2":
            header = input("\nВведите заголовок для удаления: ").strip()
            count = note_manager.delete_by_header(header)
            if count > 0:
                print(f"\nУдалено заголовков: {count}")
            else:
                print(f"\nЗаголовок '{header}' не найден")

        else:
            print("Неверный выбор. Попробуйте снова.")
class NoteField(Enum):
    USERNAME = "имя пользователя"
    CONTENT = "содержание"
    STATUS = "статус"
    CREATION_DATE = "дата создания"
    DEADLINE = "дедлайн"
    HEADERS = "заголовки"


def update_note_field(note: Note, field: str) -> None:
    """Обновляет указанное поле заметки."""
    update_handlers = {
        "имя пользователя": _update_username,
        "содержание": _update_content,
        "статус": _update_status,
        "дата создания": _update_creation_date,
        "дедлайн": _update_deadline,
        "заголовки": _update_headers
    }

    handler = update_handlers.get(field)
    if handler:
        handler(note)
    else:
        print(f"Ошибка: неизвестное поле '{field}'")
        print(f"Доступные поля: {', '.join(update_handlers.keys())}")

def _update_content(note: Note) -> None:
    """Обновляет содержимое заметки."""
    print("\nОбновление содержания (пустая строка для завершения):")
    note.contents.clear()
    while True:
        content = input("Введите заметку: ").strip()
        if not content:
            break
        if content not in note.contents:
            note.contents.append(content)
        else:
            print("Эта заметка уже существует!")

def _update_status(note: Note) -> None:
    """Обновляет статус заметки."""
    note.status = update_note_status()

def _update_username(note: Note) -> None:
    """Обновляет имя пользователя с валидацией."""
    while True:
        new_username = input("Введите новое имя пользователя: ").strip()
        if new_username:
            note.username = new_username
            break
        print("Имя пользователя не может быть пустым!")

def _update_creation_date(note: Note) -> None:
    """Обновляет дату создания с валидацией."""
    while True:
        date_str = input("Введите новую дату создания (ДД.ММ.ГГГГ, например 01.01.2024): ")
        try:
            creation_date = datetime.strptime(date_str, "%d.%m.%Y")
            if note.deadline_date:
                deadline_date = datetime.strptime(note.deadline_date, "%d.%m.%Y")
                if creation_date > deadline_date:
                    print("Ошибка: Дата создания не может быть позже даты дедлайна!")
                    continue
            note.creation_date = date_str
            break
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте формат ДД.ММ.ГГГГ")
            print("Пример: 01.01.2024")


def _update_deadline(note: Note) -> None:
    """Обновляет дату дедлайна с валидацией."""
    while True:
        date_str = input("Введите новую дату дедлайна (ДД.ММ.ГГГГ, например 01.01.2024): ")
        try:
            deadline_date = datetime.strptime(date_str, "%d.%m.%Y")
            if note.creation_date:
                creation_date = datetime.strptime(note.creation_date, "%d.%m.%Y")
                if deadline_date < creation_date:
                    print("Ошибка: Дата дедлайна не может быть раньше даты создания!")
                    continue

            note.deadline_date = date_str
            current_date = datetime.now()
            time_left = deadline_date - current_date

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
            break
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте формат ДД.ММ.ГГГГ")
            print("Пример: 01.01.2024")

def _update_headers(note: Note) -> None:
    """Обновляет заголовки заметки."""
    print("\nОбновление заголовков (пустая строка для завершения):")
    note.headers.clear()
    while True:
        header = input("Введите заголовок: ").strip()
        if not header:
            break
        if header not in note.headers:
            note.headers.append(header)
        else:
            print("Этот заголовок уже существует!")

class DateHandler:
    @staticmethod
    def format_deadline_message(deadline_date: datetime) -> str:
        current_date = datetime.now()
        time_left = deadline_date - current_date

        if deadline_date.date() == current_date.date():
            return "\nПРЕДУПРЕЖДЕНИЕ: Дедлайн истекает сегодня!"

        days = abs(time_left.days)
        if deadline_date.date() > current_date.date():
            return DateHandler._format_days_left(days)
        return DateHandler._format_days_overdue(days)

    @staticmethod
    def _format_days_left(days: int) -> str:
        if days == 1:
            return f"\nДо дедлайна остался {days} день"
        elif 2 <= days <= 4:
            return f"\nДо дедлайна осталось {days} дня"
        return f"\nДо дедлайна осталось {days} дней"

    @staticmethod
    def _format_days_overdue(days: int) -> str:
        if days == 1:
            return "\nПРЕДУПРЕЖДЕНИЕ: Дедлайн просрочен на 1 день!"
        elif 2 <= days <= 4:
            return f"\nПРЕДУПРЕЖДЕНИЕ: Дедлайн просрочен на {days} дня!"
        return f"\nПРЕДУПРЕЖДЕНИЕ: Дедлайн просрочен на {days} дней!"

def edit_note(note: Note) -> None:
    """Редактирует существующую заметку"""
    while True:
        print("\nКакое поле вы хотите изменить?")
        fields = ["имя пользователя", "содержание", "статус",
                 "дата создания", "дедлайн", "заголовки"]
        for i, field in enumerate(fields, 1):
            print(f"{i}. {field}")
        print(f"{len(fields) + 1}. Вернуться назад")

        try:
            choice = int(input("\nВаш выбор: "))
            if choice == len(fields) + 1:
                break

            if 1 <= choice <= len(fields):
                field = fields[choice - 1]
                update_note_field(note, field)
                print("\nПоле успешно обновлено!")
                display_note(note)
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def search_notes(note_manager: NoteManager) -> None:
    """Поиск заметок по ключевым словам или статусу"""
    print("\nПоиск заметок:")
    print("1. Поиск по ключевому слову")
    print("2. Поиск по статусу")
    print("3. Вернуться назад")

    choice = input("\nВаш выбор: ").strip()

    if choice == "1":
        keyword = input("Введите ключевое слово для поиска: ").strip().lower()
        found_notes = []

        for note in note_manager.notes:
            # Поиск в содержимом
            if any(keyword in content.lower() for content in note.contents):
                found_notes.append(note)
                continue

            # Поиск в заголовках
            if any(keyword in header.lower() for header in note.headers):
                found_notes.append(note)
                continue

            # Поиск в имени пользователя
            if keyword in note.username.lower():
                found_notes.append(note)

    elif choice == "2":
        print("\nДоступные статусы:")
        statuses = NoteStatus.get_status_dict().values()
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status}")

        status_choice = input("\nВыберите статус: ").strip()
        try:
            status = list(statuses)[int(status_choice) - 1]
            found_notes = [note for note in note_manager.notes if note.status == status]
        except (ValueError, IndexError):
            print("Неверный выбор статуса!")
            return
    else:
        return

    if found_notes:
        print(f"\nНайдено заметок: {len(found_notes)}")
        for i, note in enumerate(found_notes, 1):
            print(f"\nЗаметка {i}:")
            display_note(note)
    else:
        print("\nЗаметки не найдены!")

    if found_notes:
        print(f"\nНайдено заметок: {len(found_notes)}")
        for i, note in enumerate(found_notes, 1):
            print(f"\nЗаметка {i}:")
            display_note(note)
    else:
        print("\nЗаметки не найдены!")

def _update_username(note: Note) -> None:
    """Обновляет имя пользователя с валидацией."""
    while True:
        new_username = input("Введите новое имя пользователя: ").strip()
        try:
            note.username = new_username  # использует валидацию из property
            break
        except ValueError as e:
            print(f"Ошибка: {e}")