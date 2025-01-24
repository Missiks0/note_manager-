from datetime import datetime

def validate_date(date_str: str) -> datetime:
    """Проверяет корректность даты"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None

def update_note_status() -> str:
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