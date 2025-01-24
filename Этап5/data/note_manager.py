from typing import List, Optional
import json
from data.note import Note


class NoteManager:
    def __init__(self):
        self.notes: List[Note] = []

    def add_note(self, note: Note) -> None:
        """Добавляет заметку в список"""
        self.notes.append(note)

    def get_note_by_id(self, note_id: str) -> Optional[Note]:
        """Получает заметку по ID"""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def delete_note_by_id(self, note_id: str) -> bool:
        """Удаляет заметку по ID"""
        initial_length = len(self.notes)
        self.notes = [note for note in self.notes if note.id != note_id]
        return len(self.notes) < initial_length

    def delete_by_username(self, username: str) -> bool:
        """Удаляет заметки по имени пользователя"""
        initial_length = len(self.notes)
        self.notes = [note for note in self.notes if note.username.lower() != username.lower()]
        return len(self.notes) < initial_length

    def delete_by_header(self, header: str) -> int:
        """Удаляет заметки с указанным заголовком"""
        count = 0
        notes_to_remove = []

        for note in self.notes:
            if header in note.headers:
                note.headers.remove(header)
                count += 1
                if not note.headers:
                    notes_to_remove.append(note)

        for note in notes_to_remove:
            self.notes.remove(note)

        return count

    def save_notes(self, filename: str) -> None:
        """Сохраняет заметки в JSON файл"""
        notes_data = [note.to_dict() for note in self.notes]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(notes_data, f, ensure_ascii=False, indent=4)

    def get_all_notes(self) -> List[Note]:
        """Возвращает список всех заметок"""
        return self.notes

    def load_notes(self, filename: str) -> None:
        """Загружает заметки из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                notes_data = json.load(f)

            self.notes.clear()
            for note_data in notes_data:
                note = Note.from_dict(note_data)
                self.notes.append(note)
        except FileNotFoundError:
            self.notes = []