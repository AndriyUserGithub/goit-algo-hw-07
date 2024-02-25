from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def __init__(self, name: str, value):
        super().__init__(self, value)
        self.name = name


class Phone(Field):
    def __init__(self, phone, value):
        super().__init__(self, value)
        self.phone = phone

    @property
    def get_number(self):
        return self.phone

    @get_number.setter
    def setnumber(self, value):
        if len(value) == 10 and type(value) == int:
            self.phone = value
        if re.search(r'\d{10}', value) and type(value) == str:
            try:
                self.phone = int(value)
            except Exception as e:
                print("Error a number")


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d-%m-%Y').date()
        except ValueError:
            print(f"Помилка вводу: {ValueError}")
            self.value = None
            raise ValueError("Не коректний формат дати. Формат дати: ДД-ММ-РРРР")


class Record:
    def __init__(self, name, value):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, \
                Дата народження: {self.birthday.value} \
                Телефоні номери: {'; '.join(p.value for p in self.phones)}"


    def add_phone(self, phone: Phone):
        """
        Метод додає новий номер телефону
        """

        if phone.value and not self.find_phone(phone)[0]:
            self.phones.append(phone)


    def edit_phone(self, value1: str, value2: str):
        """
        Метод редагує номер телефону
        """

        phone1 = Phone(value1)
        phone2 = Phone(value2)
        phone1, i = self.find_phone(phone1)
        phone2 = self.find_phone(phone2)[0]
        if not phone1:
            self.phones[i] = phone2


    def find_phone(self, phone: Phone):
        """
        Метод шукає номер телефону
        """

        i = -1
        for p in self.phones:
            i += 1
            if phone.value == p.value:
                return (True, i)


    def remove_phone(self, phone: Phone):
        """
        Метод видаляє номер телефону
        """

        if phone is self.phones:
            self.phones.remove(phone)
        return self.phones
        

    def add_birthday(self, birthday: Birthday):
        """
        Метод додає дату дня нородження
        """

        if birthday.value:
            self.birthday = birthday
        

class AddressBook(UserDict):
    def getBook(self):
        """
        Метод задає формат інформаційної таблиці
        """
        
        titles_column = ('Name', 'Tel', 'Birthday')
        column_width = 12
        column1 = f"{titles_column[0]:<{column_width}}"
        column2 = f"{titles_column[1]:<{column_width * 2}}"
        column3 = f"{titles_column[2]:<{column_width}}"
        lines = "|" + column1 + "|" + column2 + "|" + column3 + "|\n"
        lines += "-" * len(lines) + "\n"
        for elem in self.data.items():
            first_value = f"{elem[0].value:<{column_width}}"
            second_value = f"{"; ".join(p.value for p in elem[1].phones):<{column_width * 2}}"
            third_value = f"{str(elem[1].birthday):<{column_width}}"
            lines += "|" + first_value + "|" + second_value + "|" + third_value + "|\n"        
        return lines


    def add_record(self, record: Record):
        """
        Метод додає запис в телефону книгу
        """

        key = record.name
        self.data[key] = record


    def find_record(self, name: str):
        """
        Метод шукає запис в телефоній книзі за
        іменем
        """

        for elem in self.data.items():
            if elem[0].value == name:
                return f"tel.: {'; '.join(p.value for p in elem[1].phones)}"


    def delete_record(self):
        """
        Метод видаляє запис з телефоної книги
        """

        for elem in self.data.items():
            if elem is self.data.items():
                del self.data
        return f"Запис видалено"


