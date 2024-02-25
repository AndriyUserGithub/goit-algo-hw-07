from datetime import datetime, timedelta
from console_bot_FileManager import FileManager
from console_bot_classes import Name, Record, Phone, Birthday, AddressBook


def input_error(func):
    """
    Метод - декоратор помилок
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Не корректні дані"
        except KeyError:
            return "Контактний відсутній"
        except IndexError:
            return "Індекс за межами діапазону"
        except NameError:
            return "Контакт з таким іменем відсутній"
    return inner


def get_menu_from_file(path):
    """
    Метод повертає словник даних 
    """

    menu = {}
    with FileManager(path) as fh:
        lines = fh.readlines()
    for line in lines:
        cmd, action = line.strip().split(",", 1)
        menu[cmd] = action
    return menu


def get_data_from_file(path):
    """
    Метод приймає дані з файлу, добавляє 
    в телефону книгу номер телефону та 
    інформацію про день народження
    """

    contacts = AddressBook
    with FileManager(path) as fh:
        lines = fh.readlines()
        for line in lines:
            line = line.strip().split(",") 
            name = Name(line[0])
            new_record = Record(name)
            if len(line) >= 2:
                phones = line[1].split(",")
                for phone in phones:
                    new_record.add_phone(Phone(phone))
            if len(line) >= 3:
                birthday = Birthday(line[2])
                new_record.add_birthday(birthday)
            contacts.add_record(new_record)
        return contacts


def menu(menu):
    """
    Метод задає формат для 'Меню'
    """

    print()
    print("{:^30}".format("Меню"))
    for k, v in menu.items():
        print(f"{k:<35}{v:<25}")
    print()


@input_error
def parse_input(user_input):
    """
    Метод приймає рядок вводу, розбиває
    його на слова
    """

    cmd, *args = user_input.split()
    cmd = cmd, *args


def print_contacts(contacts: AddressBook):
    """
    Метод виводить контакти 
    """

    print(contacts.getBook())


@input_error
def show_contact(args, contacts: AddressBook):
    """
    Метод шукає контакт за іменем та повертає
    дані про контакт
    """

    name = args[0]
    record_find = contacts.find_record(name)
    if record_find:
        return record_find
    else:
        raise KeyError


@input_error
def add_contact(args, contacts: AddressBook):
    """
    Метод оновлює існуючий контакт в телефоній
    книзі або додає новий контакт до телефоної 
    книги
    """

    name, phone = args
    record_find = contacts.find_record(name)
    if record_find:
        phone = Phone(phone)
        record_find.add_phone(phone)
        contacts.add_record(record_find)
        return f"Контакт {name} оновлено"
    else:
        name = Name(name)
        phone = Phone(phone)
        new_record = Record(name)
        new_record.add_phone(phone)
        contacts.add_record(new_record)
        return f"Контакт {name} додано"


@input_error
def change_contact(args, contacts: AddressBook):
    """
    Метод шукає контакт в телефоній книзі за 
    іменем та змінює його 
    """

    name, phone = args 
    phone = Phone(phone)
    if phone.value:
        record_find = contacts.find_record(name)
        if record_find:
            record_find.edit_phone(record_find.phones[0].value, phone.value)
            return f"Контакт {name} змінено"
    else:
        return f"Невірно заданий номер телефону"
    

@input_error
def del_contact(args, contacts: AddressBook):
    """
    Метод видаляє контакт з телефоної книги
    """

    name = args[0]
    contacts.del_record(name)
    return f"Контакт {name} видалено"


@input_error
def show_birthday(args, contacts: AddressBook):
    """
    Метод виводить інформацію про день народження
    контакту, за вказаним іменем
    """
    
    name = args[0]
    rec_find = contacts.find_record(name)
    return rec_find.birthday.value.strftime("%d-%m-%Y")


@input_error
def birthdays(contacts: AddressBook):
    """
    Метод приймає словник з інформацією про день 
    народження за іменем контакту та повертає 
    список контактів, яких потрібно привітати 
    на поточному тижні 
    """
    
    today = datetime.today().date()
    congratulation_list = []

    for user in contacts.data.items():
        if user[1].birthday:
            congratulation_user_dict = {}
            dict_keys = ("Ім'я", "День Народження")
            user_birthday = user[1].birthday.value
            if user_birthday:
                birthday_this_year = datetime(year = today.year, \
                                              month = user_birthday.month, \
                                                day = user_birthday.day).date()
                
                if birthday_this_year < today:
                    continue
                elif birthday_this_year.toordinal() - today.toordinal() > 7:
                    continue
                else:
                    congratulation_date = datetime(year = today.year, \
                                                   month = birthday_this_year.month, \
                                                    day = birthday_this_year.day).date()
                    if congratulation_date.weekday() == 6:
                        congratulation_date += timedelta(days = 1)
                    elif congratulation_date.weekday() == 5:
                        congratulation_date += timedelta(days = 2)

                    congratulation_date = congratulation_date.strftime("%d-%m-%Y")
                    congratulation_user_dict.update({dict_keys[0]: user[1].name, \
                                                     dict_keys[1]: congratulation_date})
                    congratulation_list.append(congratulation_user_dict)
    if congratulation_list:
        return f"\n".join(map(str, congratulation_list))
    else:
        return f"На цьому тижні імениники відсутні"
    

@input_error
def add_birthday(args, contacts: AddressBook):
    """
    Метод шукає контакт за іменем та додає до контакту
    інформацію про день народження
    """
    
    name = args[0]
    birthday = args[1]
    record_find = contacts.find_record(name)
    if record_find:
        record_find.add_birthday(Birthday(birthday))
        print(f"Для {name} задано дату народження {birthday}")


def rewrite_contacts(path, contacts: AddressBook):
    """
    Метод добавляє інформацію про день народження 
    до файлу з контактами
    """
    
    lines = []
    for k in contacts.data.items():
        name = k[1].name
        phones = f"{'; '.join(p.value for p in k[1].phones)}"
        line = f"{name}, {phones}"
        birthday = k[1].birthday.value if k[1].birthday else ""
        if birthday:
            birthday = birthday.strftime("%d-%m-%Y")
            line += f",{birthday}"
        lines.append(line)
    with FileManager(path, mode = "w") as fh:
        fh.writelines("\n".join(lines))


        
        