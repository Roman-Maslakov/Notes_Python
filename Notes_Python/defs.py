from datetime import datetime

PATH = 'Notes_Python\\notes.csv'

def input_command():
    command = input("  ")
    match command:
        case "add":
            add_note()
            print("\n  Готов к работе")
            return True
        case "open":
            open_notes()
            print("\n  Готов к работе")
            return True
        case "open old":
            open_first(1)
            print("\n  Готов к работе")
            return True
        case "open new":
            open_first(-1)
            print("\n  Готов к работе")
            return True
        case "select":
            select_note()
            print("\n  Готов к работе")
            return True
        case "delete":
            delete_note()
            print("\n  Готов к работе")
            return True
        case "edit":
            edit_note()
            print("\n  Готов к работе")
            return True
        case "":
            print("  -----------\n  До свидания")
            return False
        case other:
            tab = "-" * 58
            print("  " + tab + "\n  Неизвестная команда, выберите команду из предложенных выше")
            print("\n  Готов к работе")
            return True

def get_id():
    with open(PATH, 'r', encoding="UTF-8") as f:
        data = f.readlines()
        if len(data) != 0:
            return int(data[-1].split(";")[0])
        else:
            return 0

def add_note():
    id = get_id() + 1
    date = datetime.now()
    header = input("  Заголовок: ")
    note = input("  Содержание: ")
    with open(PATH, 'a', encoding="UTF-8") as f:
        f.write(str(id) + ";" + header +  ";" + note + ";" + "дата/время создания: " + date.strftime("%d/%m/%y %H:%M:%S") + "\n")
        print("  ---------------\n  Заметка создана")
            
def open_notes():
    if check_file():
        flag = True
        date = input("  Введите дату или диапозон в формате dd/mm/yy или dd/mm/yy - dd/mm/yy соответственно\n")
        if check_date(date):
            with open(PATH, 'r', encoding="UTF-8") as f:
                print()
                parsed_date = parse_date(date)
                data = f.readlines()
                sorted_data = sort_data(data, parsed_date)
                for data_line in sorted_data:
                    flag = False
                    note = data_line.split(";")
                    print(f"Заметка {note[0]}: {note[1]} - {note[3]}")
                if flag:
                    print("  В это время заметок не было")
        else:
            print("  Вы некорректно ввели дату")

def select_note():
    if check_file():
        note_id = input("\n  Введите номер заметки: ")
        flag = True
        with open(PATH, 'r', encoding="UTF-8") as f:
            data = f.readlines()
            for data_line in data:
                if data_line.split(";")[0] == note_id:
                    flag = False
                    print(f"\nЗаметка {data_line.split(';')[0]}: {data_line.split(';')[1]}")
                    print("  " + data_line.split(';')[2])
        if flag:
            print("  " + "-" * 35)
            print("  Заметки с данным номером не нашлось")
    
def open_first(min_or_max):
    if check_file():
        with open(PATH, 'r', encoding="UTF-8") as f:
            data = sort_by(f.readlines(), min_or_max)
            for data_line in data:
                    note = data_line.split(";")
                    print(f"Заметка {note[0]}: {note[1]} - {note[3]}")

def delete_note():
    if check_file():
        note_id = input("\n  Введите номер заметки: ")
        flag = True
        with open(PATH, 'r', encoding="UTF-8") as f:
            data = f.readlines()
            for i in range(len(data)):
                    if data[i].split(";")[0] == note_id:
                        flag = False
                        data[i] = ""
                        re_write(data)
                        update_ids(note_id)
                        print("  " + "-" * 15 + "\n  Заметка удалена")
            if flag:
                print("  " + "-" * 35)
                print("  Заметки с данным номером не нашлось")

def edit_note():
    if check_file():
        note_id = input("\n  Введите номер заметки: ")
        flag = True
        with open(PATH, 'r', encoding="UTF-8") as f:
            data = f.readlines()
            for i in range(len(data)):
                    if data[i].split(";")[0] == note_id:
                        flag = False
                        date = datetime.now()
                        header = input("  Заголовок: ")
                        note = input("  Содержание: ")
                        data[i] = (note_id + ";" + header +  ";" + note + ";" 
                        + "дата/время изменения: " + date.strftime("%d/%m/%y %H:%M:%S") + "\n")
                        re_write(data)
                        print("  " + "-" * 21 + "\n  Заметка редактирована")
            if flag:
                print("  " + "-" * 35)
                print("  Заметки с данным номером не нашлось")
        
def re_write(old_data):
    new_data = ""
    for data_line in old_data:
        new_data += data_line
    with open(PATH, 'w', encoding="UTF-8") as f:
        f.write(new_data)

def update_ids(current_id):
    current_id = int(current_id)
    with open(PATH, 'r', encoding="UTF-8") as f:
        data = f.readlines()
        for i in range(current_id - 1, len(data)):
            data[i] = data[i].replace(str(current_id + 1), str(current_id), 1)
            current_id += 1
    re_write(data)

def check_file():
    with open(PATH, 'r', encoding="UTF-8") as f:
        if len(f.read()) == 0:
            print("  " + "-" * 73)
            print("  В заметках пусто, чтобы создать новую заметку воспользуйтесь командой add")
            return False
        else:
            return True

def check_date(date_str: str):
    check = date_str.split("-")
    match len(check):
        case 1:
            check = check[0].split("/")
            try:
                if int(check[0]) > 31 or int(check[1]) > 12 or int(check[2]) > 23:
                    return False
                else:
                    return True
            except ValueError:
                return False
        case 2:
            try:
                if int(check[0].split("/")[0]) > 31 or int(check[0].split("/")[1]) > 12 or int(check[0].split("/")[2]) > 23:
                    return False
                if int(check[1].split("/")[0]) > 31 or int(check[1].split("/")[1]) > 12 or int(check[1].split("/")[2]) > 23:
                    return False
                else:
                    return True
            except ValueError:
                return False
            
def parse_date(date_str: str):
    date = date_str.split("-")
    if len(date) == 1:
        date = date[0].split("/")
        date = [int(date[0]) + (int(date[1]) * 31) + (int(date[2]) * 372)] # все месяцы приравнял к 31, получается год 372 дня
        return date  
    else: 
        date[0] = date[0].split("/")
        date[1] = date[1].split("/")
        date[0] = int(date[0][0]) + (int(date[0][1]) * 31) + (int(date[0][2]) * 372)
        date[1] = int(date[1][0]) + (int(date[1][1]) * 31) + (int(date[1][2]) * 372)
        return date
    
def sort_data(data_list, sort_by):
    res = list()
    if len(sort_by) == 1:
        for data_line in data_list:
            if parse_date(data_line.split(";")[3].split(" ")[2]) == sort_by:
                res.append(data_line)
        return res
    else:
        for data_line in data_list:
            if sort_by[0] <= parse_date(data_line.split(";")[3].split(" ")[2])[0] <= sort_by[1]:
                res.append(data_line)
        return res
   
def sort_by(data_list, min_or_max):
    for i in range(len(data_list) - 1):
        min = i
        for j in range(i + 1, len(data_list)):
            if min_or_max*parse_date(data_list[j].split(";")[3].split(" ")[2])[0] < min_or_max*parse_date(data_list[min].split(";")[3].split(" ")[2])[0]:
                min = j
        data_list[i], data_list[min] = data_list[min], data_list[i]
    return data_list