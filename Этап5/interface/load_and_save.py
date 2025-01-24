import json
from typing import Any, Callable, Dict, List
from data.note import Note

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

    except PermissionError:
        print(f"\nОшибка: нет прав доступа к файлу {filename}")
        return False
    except Exception as e:
        print(f"\nОшибка при сохранении заметок: {str(e)}")
        return False


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
            try:
                note = Note()
                note.username = note_dict['username']
                note.contents = note_dict['contents']
                note.headers = note_dict['headers']
                note.status = note_dict['status']
                note.creation_date = note_dict['creation_date']
                note.deadline_date = note_dict['deadline_date']
                notes.append(note)
            except KeyError:
                print(f"\nОшибка при чтении файла {filename}. Проверьте его содержимое.")
                return []

        print(f"\nЗаметки успешно загружены из файла {filename}")
        return notes

    except FileNotFoundError:
        print(f"\nФайл {filename} не найден. Создан новый файл.")
        save_notes_to_file([], filename)
        return []
    except json.JSONDecodeError:
        print(f"\nОшибка при чтении файла {filename}. Проверьте его содержимое.")
        return []
    except PermissionError:
        print(f"\nОшибка: нет прав доступа к файлу {filename}")
        return []
    except Exception as e:
        print(f"\nОшибка при загрузке заметок: {str(e)}")
        return []


def append_notes_to_file(notes: List[Note], filename: str) -> bool:
    """
    Добавляет новые заметки в существующий файл без удаления старых.

    Args:
        notes: Список новых заметок для добавления
        filename: Имя файла

    Returns:
        bool: True если добавление успешно, False в случае ошибки
    """
    try:
        # Сначала читаем существующие заметки
        existing_notes = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                for note_dict in existing_data:
                    note = Note()
                    note.username = note_dict['username']
                    note.contents = note_dict['contents']
                    note.headers = note_dict['headers']
                    note.status = note_dict['status']
                    note.creation_date = note_dict['creation_date']
                    note.deadline_date = note_dict['deadline_date']
                    existing_notes.append(note)
        except FileNotFoundError:
            print(f"\nФайл {filename} не найден. Будет создан новый файл.")
        except json.JSONDecodeError:
            print(f"\nОшибка при чтении файла {filename}. Файл будет перезаписан.")

        # Объединяем существующие и новые заметки
        all_notes = existing_notes + notes

        # Преобразуем все заметки в список словарей
        notes_data = []
        for note in all_notes:
            note_dict = {
                'username': note.username,
                'contents': note.contents,
                'headers': note.headers,
                'status': note.status,
                'creation_date': note.creation_date,
                'deadline_date': note.deadline_date
            }
            notes_data.append(note_dict)

        # Записываем объединенный список обратно в файл
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(notes_data, file, ensure_ascii=False, indent=4)

        print(f"\nЗаметки успешно добавлены в файл {filename}")
        return True

    except PermissionError:
        print(f"\nОшибка: нет прав доступа к файлу {filename}")
        return False
    except Exception as e:
        print(f"\nОшибка при добавлении заметок: {str(e)}")
        return False