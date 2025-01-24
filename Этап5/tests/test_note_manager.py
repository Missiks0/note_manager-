import unittest
import os
from datetime import datetime
from data.note import Note
from data.note_manager import NoteManager
from utils.helpers import validate_date


class TestNoteManager(unittest.TestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.note_manager = NoteManager()
        self.test_note = Note()
        self.test_note.username = "Test User"
        self.test_note.contents = ["Test Content"]
        self.test_note.headers = ["Test Header"]
        self.test_note.status = "в процессе"
        self.test_note.creation_date = "01.01.2024"
        self.test_note.deadline_date = "31.12.2024"

    def test_delete_by_header(self):
        """Тест удаления заметки по заголовку"""
        # Создаем заметку с двумя заголовками
        note = Note()
        note.username = "Test User"
        note.headers = ["Header 1", "Header 2"]
        self.note_manager.add_note(note)

        # Создаем вторую заметку с одним из тех же заголовков
        note2 = Note()
        note2.username = "Test User 2"
        note2.headers = ["Header 1", "Header 3"]
        self.note_manager.add_note(note2)

        # Удаляем заголовок, который есть у обеих заметок
        count = self.note_manager.delete_by_header("Header 1")
        self.assertEqual(count, 2)  # Заголовок удален из двух заметок
        self.assertEqual(len(self.note_manager.notes), 2)  # Обе заметки все еще существуют
        self.assertEqual(self.note_manager.notes[0].headers, ["Header 2"])
        self.assertEqual(self.note_manager.notes[1].headers, ["Header 3"])

        # Удаляем оставшийся заголовок у первой заметки
        count = self.note_manager.delete_by_header("Header 2")
        self.assertEqual(count, 1)
        self.assertEqual(len(self.note_manager.notes), 1)  # Первая заметка удалена
        
    def test_add_note(self):
        """Тест добавления заметки"""
        initial_count = len(self.note_manager.notes)
        self.note_manager.add_note(self.test_note)
        self.assertEqual(len(self.note_manager.notes), initial_count + 1)
        self.assertEqual(self.note_manager.notes[-1], self.test_note)

    def test_delete_by_username(self):
        """Тест удаления заметки по имени пользователя"""
        self.note_manager.add_note(self.test_note)
        result = self.note_manager.delete_by_username("Test User")
        self.assertTrue(result)
        self.assertEqual(len(self.note_manager.notes), 0)

    def test_delete_nonexistent_username(self):
        """Тест удаления несуществующего пользователя"""
        self.note_manager.add_note(self.test_note)
        result = self.note_manager.delete_by_username("Nonexistent User")
        self.assertFalse(result)
        self.assertEqual(len(self.note_manager.notes), 1)


class TestValidation(unittest.TestCase):
    def test_date_validation(self):
        """Тест валидации даты"""
        # Правильные даты
        self.assertIsInstance(validate_date("01.01.2024"), datetime)
        self.assertIsInstance(validate_date("31.12.2024"), datetime)

        # Неправильные даты
        self.assertIsNone(validate_date("32.01.2024"))  # несуществующий день
        self.assertIsNone(validate_date("01.13.2024"))  # несуществующий месяц
        self.assertIsNone(validate_date("01.01.24"))  # неправильный формат года
        self.assertIsNone(validate_date("2024.01.01"))  # неправильный формат
        self.assertIsNone(validate_date("invalid"))  # невалидная строка


class TestNoteStorage(unittest.TestCase):
    def setUp(self):
        self.note_manager = NoteManager()
        self.test_file = "test_notes.json"
        self.test_note = Note()
        self.test_note.username = "Test User"
        self.test_note.contents = ["Test Content"]
        self.test_note.headers = ["Test Header"]
        self.test_note.status = "в процессе"
        self.test_note.creation_date = "01.01.2024"
        self.test_note.deadline_date = "31.12.2024"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_notes(self):
        """Тест сохранения и загрузки заметок"""
        self.note_manager.add_note(self.test_note)
        self.note_manager.save_notes(self.test_file)

        new_manager = NoteManager()
        new_manager.load_notes(self.test_file)

        self.assertEqual(len(new_manager.notes), 1)
        loaded_note = new_manager.notes[0]

        self.assertEqual(loaded_note.username, self.test_note.username)
        self.assertEqual(loaded_note.contents, self.test_note.contents)
        self.assertEqual(loaded_note.headers, self.test_note.headers)
        self.assertEqual(loaded_note.status, self.test_note.status)
        self.assertEqual(loaded_note.creation_date, self.test_note.creation_date)
        self.assertEqual(loaded_note.deadline_date, self.test_note.deadline_date)


def test_note_id_generation(self):
    """Тест генерации уникальных ID"""
    note1 = Note()
    note2 = Note()
    self.assertNotEqual(note1.id, note2.id)
    self.assertTrue(isinstance(note1.id, str))
    self.assertTrue(len(note1.id) > 0)


def test_get_note_by_id(self):
    """Тест получения заметки по ID"""
    note = Note()
    note.username = "Test User"
    self.note_manager.add_note(note)

    found_note = self.note_manager.get_note_by_id(note.id)
    self.assertIsNotNone(found_note)
    self.assertEqual(found_note.id, note.id)
    self.assertEqual(found_note.username, note.username)


def test_delete_note_by_id(self):
    """Тест удаления заметки по ID"""
    note = Note()
    note.username = "Test User"
    self.note_manager.add_note(note)

    result = self.note_manager.delete_note_by_id(note.id)
    self.assertTrue(result)
    self.assertEqual(len(self.note_manager.notes), 0)

if __name__ == '__main__':
    unittest.main()