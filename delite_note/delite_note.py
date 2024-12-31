

from datetime import datetime


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


def main():
    global note_manager
    note_manager = NoteManager()

    while True:
        print("\nДоступные действия:")
        print("1. Создать новую заметку")
        print("2. Удалить заметку")
        print("3. Показать все заметки")
        print("4. Выйти")

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
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()