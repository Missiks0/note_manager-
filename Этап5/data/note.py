import uuid

class Note:
    def __init__(self):
        self.id = str(uuid.uuid4())  # Добавляем уникальный идентификатор
        self.username = ""
        self.contents = []
        self.headers = []
        self.status = "в процессе"
        self.creation_date = None
        self.deadline_date = None

    def to_dict(self) -> dict:
        """Преобразует заметку в словарь для сохранения"""
        return {
            'id': self.id,
            'username': self.username,
            'contents': self.contents,
            'headers': self.headers,
            'status': self.status,
            'creation_date': self.creation_date,
            'deadline_date': self.deadline_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
            """Создает заметку из словаря"""
            note = cls()
            note.id = data.get('id', str(uuid.uuid4()))  # Если ID нет, создаем новый
            note.username = data['username']
            note.contents = data['contents']
            note.headers = data['headers']
            note.status = data['status']
            note.creation_date = data['creation_date']
            note.deadline_date = data['deadline_date']
            return note

    def delete_by_header(self, header: str) -> bool:
        """Удаляет заголовок из заметки"""
        if header in self.headers:
            self.headers.remove(header)
            return True
        return False

    def matches_username(self, username: str) -> bool:
        """Проверяет, принадлежит ли заметка указанному пользователю"""
        return self.username.lower() == username.lower()