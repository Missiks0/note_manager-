#ввод данных
note = []

username = input("Введите имя пользователя: ")
note.append(username)

content = input("Введите содержание заметки: ")
note.append(content)

status = input("Введите статус заметки: ")
note.append(status)
#цикл для заметок
new_status = input("Введите новый статус заметки (или Enter чтобы оставить текущий): ")
if new_status:
    note[2] = new_status
    print(f"Статус изменен на: {new_status}")

creation_date = input("Введите дату заметки в формате ДД.ММ.ГГГГ: ")
note.append(creation_date)

modification_date = input("Введите дату изменения в формате ДД.ММ.ГГГГ: ")
note.append(modification_date)
#цикл для заголовков(loop)
headers = []
while True:
    header = input("Введите заголовок (или Enter для завершения): ")
    if header == "":
        break
    headers.append(header)
note.append(headers)
#вывод данных
print("\nИнформация о заметке:")
print(f"Имя пользователя: {note[0]}")
print(f"Содержание: {note[1]}")
print(f"Статус: {note[2]}")
print(f"Дата создания: {note[3]}")
print(f"Дата изменения: {note[4]}")
print("Заголовки:")
for header in note[5]:
    print(f"- {header}")