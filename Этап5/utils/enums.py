from enum import Enum

class NoteStatus(Enum):
    DONE = "выполнено"
    IN_PROGRESS = "в процессе"
    POSTPONED = "отложено"

class NoteField(Enum):
    USERNAME = "имя пользователя"
    CONTENT = "содержание"
    STATUS = "статус"
    CREATION_DATE = "дата создания"
    DEADLINE = "дедлайн"
    HEADERS = "заголовки"