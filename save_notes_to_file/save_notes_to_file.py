from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List
import json


class NoteStatus(Enum):
    DONE = "выполнено"
    IN_PROGRESS = "в процессе"
    POSTPONED = "отложено"

    @classmethod
    def get_status_dict(cls) -> dict:
        return {
            1: cls.DONE.value,
            2: cls.IN_PROGRESS.value,
            3: cls.POSTPONED.value
        }


class Note:
    def __init__(self):
        self.username = ""
        self.contents = []
        self.headers = []
        self.status = "в процессе"
        self.creation_date = None
        self.deadline_date = None

    def delete_by_header(self, header: str) -> bool:
        """Удаляет заголовок из заметки"""
        if header in self.headers:
            self.headers.remove(header)
            return True
        return False

    def matches_username(self, username: str) -> bool:
        """Проверяет, принадлежит ли заметка указанному пользователю"""
        return self.username.lower() == username.lower()


class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, note: Note):
        """Добавляет новую заметку в список"""
        self.notes.append(note)

    def delete_by_username(self, username: str) -> bool:
        """Удаляет все заметки указанного пользователя"""
        initial_length = len(self.notes)
        self.notes = [note for note in self.notes if not note.matches_username(username)]
        return len(self.notes) < initial_length

    def delete_by_header(self, header: str) -> int:
        """Удаляет заметки с указанным заголовком"""
        count = 0
        for note in self.notes:
            if note.delete_by_header(header):
                count += 1
        # Удаляем заметки без заголовков
        self.notes = [note for note in self.notes if note.headers]
        return count


def validate_date(date_str):
    """Проверяет корректность даты"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None


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


def handle_deletion():
    """Обработка удаления заметок"""
    while True:
        print("\nВыберите способ удаления:")
        print("1. Удалить по имени пользователя")
        print("2. Удалить по заголовку")
        print("3. Вернуться назад")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            username = input("Введите имя пользователя: ").strip()
            if note_manager.delete_by_username(username):
                print(f"\nУспешно удалены все заметки пользователя {username}")
            else:
                print(f"\nЗаметки пользователя {username} не найдены")

        elif choice == "2":
            header = input("Введите заголовок для удаления: ").strip()
            count = note_manager.delete_by_header(header)
            if count > 0:
                print(f"\nУдалено заметок с заголовком '{header}': {count}")
            else:
                print(f"\nЗаметки с заголовком '{header}' не найдены")

        elif choice == "3":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


def display_all_notes():
    """Отображает все существующие заметки"""
    if not note_manager.notes:
        print("\nСписок заметок пуст")
        return

    print("\nВсе существующие заметки:")
    for i, note in enumerate(note_manager.notes, 1):
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

    # Ввод дат
    while True:
        date_str = input("Введите дату создания в формате ДД.ММ.ГГГГ: ")
        creation_date = validate_date(date_str)
        if creation_date:
            note.creation_date = date_str
            break
        print("Ошибка: Неверный формат даты")

    while True:
        date_str = input("Введите дату дедлайна в формате ДД.ММ.ГГГГ: ")
        deadline_date = validate_date(date_str)
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


class NoteField(Enum):
    USERNAME = "имя пользователя"
    CONTENT = "содержание"
    STATUS = "статус"
    CREATION_DATE = "дата создания"
    DEADLINE = "дедлайн"
    HEADERS = "заголовки"


def update_note_field(note: Note, field: str) -> None:
    """
    Обновляет указанное поле заметки с соответствующей валидацией.

    Args:
        note: Заметка для обновления
        field: Поле для обновления (из NoteField)
    """
    update_handlers: Dict[str, Callable[[Note], None]] = {
        NoteField.USERNAME.value: _update_username,
        NoteField.CONTENT.value: _update_content,
        NoteField.STATUS.value: _update_status,
        NoteField.CREATION_DATE.value: _update_creation_date,
        NoteField.DEADLINE.value: _update_deadline,
        NoteField.HEADERS.value: _update_headers
    }

    handler = update_handlers.get(field)
    if handler:
        handler(note)
    else:
        print(f"Ошибка: неизвестное поле '{field}'")
        print(f"Доступные поля: {', '.join(f.value for f in NoteField)}")


def _update_username(note: Note) -> None:
    """Обновляет имя пользователя с валидацией."""
    while True:
        new_username = input("Введите новое имя пользователя: ").strip()
        try:
            note.username = new_username  # использует валидацию из property
            break
        except ValueError as e:
            print(f"Ошибка: {e}")


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


def _update_creation_date(note: Note) -> None:
    """Обновляет дату создания с валидацией."""
    while True:
        date_str = input("Введите новую дату создания (ДД.ММ.ГГГГ): ")
        if date := validate_date(date_str):
            note.creation_date = date_str
            break
        print("Ошибка: Неверный формат даты")


def _update_deadline(note: Note) -> None:
    """Обновляет дату дедлайна с валидацией и уведомлением."""
    while True:
        date_str = input("Введите новую дату дедлайна (ДД.ММ.ГГГГ): ")
        if deadline_date := validate_date(date_str):
            note.deadline_date = date_str
            print(DateHandler.format_deadline_message(deadline_date))
            break
        print("Ошибка: Неверный формат даты")


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
        for i, field in enumerate(NoteField, 1):
            print(f"{i}. {field.value}")
        print(f"{len(NoteField) + 1}. Вернуться назад")

        try:
            choice = int(input("\nВаш выбор: "))
            if choice == len(NoteField) + 1:
                break

            if 1 <= choice <= len(NoteField):
                field = list(NoteField)[choice - 1].value
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


def load_notes_from_file(filename: str) -> List[Note]:
    """
    Загружает список заметок из текстового файла.

    Args:
        filename: Имя файла для загрузки

    Returns:
        List[Note]: Список загруженных заметок
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            notes_data = json.load(file)

        notes = []
        for note_dict in notes_data:
            note = Note()
            note.username = note_dict['username']
            note.contents = note_dict['contents']
            note.headers = note_dict['headers']
            note.status = note_dict['status']
            note.creation_date = note_dict['creation_date']
            note.deadline_date = note_dict['deadline_date']
            notes.append(note)

        print(f"\nЗаметки успешно загружены из файла {filename}")
        return notes

    except FileNotFoundError:
        print(f"\nФайл {filename} не найден")
        return []
    except Exception as e:
        print(f"\nОшибка при загрузке заметок: {str(e)}")
        return []


def save_notes_to_file(notes: List[Note], filename: str) -> bool:
    """
    Записывает список заметок в текстовый файл в формате JSON.

    Args:
        notes: Список заметок для сохранения
        filename: Имя файла для сохранения

    Returns:
        bool: True если сохранение успешно, False в случае ошибки
    """
    try:
        # Преобразуем заметки в список словарей
        notes_data = []
        for note in notes:
            note_dict = {
                'username': note.username,
                'contents': note.contents,
                'headers': note.headers,
                'status': note.status,
                'creation_date': note.creation_date,
                'deadline_date': note.deadline_date
            }
            notes_data.append(note_dict)

        # Записываем в файл
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(notes_data, file, ensure_ascii=False, indent=4)

        print(f"\nЗаметки успешно сохранены в файл {filename}")
        return True

    except Exception as e:
        print(f"\nОшибка при сохранении заметок: {str(e)}")
        return False


def main():
    global note_manager
    note_manager = NoteManager()

    # Пытаемся загрузить заметки при запуске
    notes = load_notes_from_file('notes.json')
    if notes:
        note_manager.notes = notes

    while True:
        print("\nДоступные действия:")
        print("1. Создать новую заметку")
        print("2. Удалить заметку")
        print("3. Показать все заметки")
        print("4. Редактировать заметку")
        print("5. Поиск заметок")
        print("6. Сохранить заметки в файл")
        print("7. Загрузить заметки из файла")
        print("8. Выйти")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            note = create_note()
            note_manager.add_note(note)
            print("\nЗаметка успешно создана:")
            display_note(note)

        elif choice == "2":
            handle_deletion()

        elif choice == "3":
            display_all_notes()

        elif choice == "4":
            if not note_manager.notes:
                print("\nСписок заметок пуст!")
                continue

            print("\nВыберите заметку для редактирования:")
            for i, note in enumerate(note_manager.notes, 1):
                print(f"\n{i}. Заметка:")
                display_note(note)

            try:
                choice = int(input("\nВведите номер заметки: "))
                if 1 <= choice <= len(note_manager.notes):
                    edit_note(note_manager.notes[choice - 1])
                else:
                    print("Неверный номер заметки!")
            except ValueError:
                print("Пожалуйста, введите число.")

        elif choice == "5":
            if not note_manager.notes:
                print("\nСписок заметок пуст!")
                continue
            search_notes(note_manager)

        elif choice == "6":
            save_notes_to_file(note_manager.notes, 'notes.json')

        elif choice == "7":
            notes = load_notes_from_file('notes.json')
            if notes:
                note_manager.notes = notes

        elif choice == "8":
            # Сохраняем заметки перед выходом
            save_notes_to_file(note_manager.notes, 'notes.json')
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()