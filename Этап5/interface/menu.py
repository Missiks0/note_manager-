from data.note_manager import NoteManager
from interface.load_and_save import load_notes_from_file
from interface.notes import display_note
from interface.notes import create_note
from interface.notes import handle_deletion
from interface.notes import display_all_notes
from interface.notes import edit_note
from interface.notes import search_notes
from interface.load_and_save import save_notes_to_file

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
            handle_deletion(note_manager)

        elif choice == "3":
            display_all_notes(note_manager)

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