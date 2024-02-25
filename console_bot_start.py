import re
from pathlib import Path 
from console_bot_functions import\
    get_data_from_file,\
    get_menu_from_file,\
    parse_input,\
    rewrite_contacts,\
    print_contacts,\
    show_contact,\
    add_contact,\
    del_contact,\
    show_birthday,\
    birthdays,\
    add_birthday
    

def main():
    data_dir = Path()
    data_file = Path()
    data_path = data_dir / data_file
    contacts = get_data_from_file(data_path)

    changes = False

    menu_file = 'cli_menu'
    menu_path = data_dir / menu_file
    menu = get_menu_from_file(menu_path) 

    print('Консольний бот-помічник') 

    while True:
        print(menu)
        user_input = input('Введіть команду: ') 
        command, *args = parse_input(user_input)
        if command in ['close', 'exit']:
            if changes:
                answer = input('Зберегти зміни? y/n')
                if answer.lower() == 'y':
                    rewrite_contacts(data_path, contacts)
            return print("До побаченя")
            break
        elif command == "hello":
            print("Чим я можу допомогти?")
        elif command == "all":
            print(print_contacts(contacts))
        elif command == "show":
            print(show_contact(args, contacts))
        elif command == "add":
            print(add_contact(args, contacts))
            changes = True
        elif command == "del":
            print(del_contact(args, contacts))
            changes = True
        elif command == "show-birthday" and args:
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        elif command == "add-birthday" and args:
            print(add_birthday(args, contacts))
            changes = True
        else:
            print("Не вірна команда")


if __name__ == "__main__":
    main()






