from collections import UserDict
import re
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class Name(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value_to_check):
        if len(value_to_check) <= 20:
            self._value = value_to_check
        else:
            print("Будь ласка, вкажіть ім'я коротше 20 знаків")
            raise ValueError


class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value_to_check):
        regex = "^[0-9\+\-\(\)]+$"
        result = re.fullmatch(regex, value_to_check)
        if result:
            if len(value_to_check) <= 40:
                self.__value = value_to_check
            else:
                print('Помилка у номері. Номер має не має бути довший 40 символів')
                raise ValueError
        else:
            print('Помилка у номері. Номер має складатися з цифр, знаків "+", "-", "(" та ")"')
            raise ValueError
        
    def __str__(self):
        return self.value


class Birthday:
    def __init__(self, value):
        self._value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            print('День народження вказаний у неправильному форматі. Будь ласка, вкажіть у форматі ДД.ММ.РРРР')
            raise ValueError
    
    # def __str__(self):
    #     return self._value.strftime("%d.%m.%Y")
    
    # def __repr__(self):
    #     return self._value.strftime("%d.%m.%Y")


class Record:
    def __init__(self,
                 name: Name,
                 phone: Phone = None,
                 birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == phone.value:
                ph_count += 1
        if not ph_count:
            self.phones.append(phone)
            return f'Я додав номер {phone.value} до списку контактів у {self.name}'
        return f'Номер {phone.value} вже є у списку контактів у {self.name}'
    
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == new_phone.value:
                ph_count += 1
        if ph_count:
            return f'Номер {new_phone.value}, який ти хочеш додати замість {old_phone.value}, вже є у списку контактів у {self.name}'
        for phone_number in self.phones:
            if phone_number.value == old_phone.value:
                phone_number.value = new_phone.value
                return f'Я замінив номер {old_phone.value} на {new_phone.value} у списку контактів у {self.name}'
        return f'Я не знайшов номер {old_phone.value} у списку контактів у {self.name}'

    def del_phone(self, phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == phone.value:
                ph_count += 1
        if ph_count:
            for i in range(len(self.phones)):
                if self.phones[i].value == phone.value:
                    self.phones.pop(i)
                    return f'Я видалив номер {phone} у {self.name}'
                else:
                    continue
            return f'Я не знайшов номер {phone} у {self.name}'
        else:
            return f'Номеру {phone.value}, який ти хочеш видалити, немає у списку контактів у {self.name}'
        
    def add_birthday(self, birthday: Birthday):
        if self.birthday and self.birthday.value.strftime("%d.%m.%Y") != "01.01.0001":
            return f'У {self.name} вже введений день народження {self.birthday.value.strftime("%d.%m.%Y")}. Для зміни використай команду "bdchange"'
        self.birthday = birthday
        return f'Я додав день народження {birthday.value.strftime("%d.%m.%Y")} до списку контактів у {self.name}'
    
    def change_birthday(self, new_birthday: Birthday):
        if self.birthday:
            old_birthday = str(self.birthday.value.strftime("%d.%m.%Y"))
            self.birthday = new_birthday
            return f'Я замінив день народження {old_birthday} на {new_birthday} у {self.name}'
        self.birthday = new_birthday
        return f'Я додав день народження {new_birthday} до списку контактів у {self.name}'
    
    def del_birthday(self, birthday: Birthday):
        if self.birthday:
            birthday_to_del = self.birthday.value.strftime("%d.%m.%Y")
            self.birthday.value = "01.01.0001"
            return f'Я видалив день народження {birthday_to_del} у {self.name}'
        return f'У {self.name} не введений день народження'
    
    def days_to_birthday(self, name: str):
        if self.birthday is None or self.birthday.value.strftime("%d.%m.%Y") == "01.01.0001":
            return f'Для контакту {name} не вказаний день народження'
        else:
            today_date = datetime.now().date()
            birth_date_ = str(self.birthday.value.strftime("%d.%m.%Y"))
            birth_date = datetime.strptime(birth_date_, "%d.%m.%Y")
            next_birthday_date = datetime(today_date.year, birth_date.month, birth_date.day).date()
            if next_birthday_date < today_date:
                next_birthday_date = datetime(today_date.year + 1, birth_date.month, birth_date.day).date()
            timedelta = next_birthday_date - today_date
            if timedelta.days == 0:
                return f"Сьогодні день народження у {name}!"
            elif timedelta.days == 1:
                return f"Завтра день народження у {name}"
            elif timedelta.days == 2:
                return f"Післязавтра день народження у {name}"
            elif timedelta.days == 3:
                return f"Через {timedelta.days} дні день народження у {name}!"
            elif timedelta.days == 4:
                return f"Через {timedelta.days} дні день народження у {name}!"
            elif timedelta.days == -1:
                return f"Учора був день народження у {name}"
            else:
                return f'Наступний день народження у {name} {next_birthday_date.strftime("%d.%m.%Y")}, через {timedelta.days} днів'
    
    def __str__(self):
        if self.phones and self.birthday and self.birthday.value.strftime("%d.%m.%Y") != "01.01.0001":
            return f"{self.name}: телефон/-и {', '.join(str(phone) for phone in self.phones)}. День народження {self.birthday.value.strftime('%d.%m.%Y')}" # {self.birthday.strftime('%d.%m.%Y')}
        if self.phones and not self.birthday:
            return f"{self.name}: телефон/-и {', '.join(str(phone) for phone in self.phones)}"
        if self.phones and self.birthday.value.strftime("%d.%m.%Y") == "01.01.0001":
            return f"{self.name}: телефон/-и {', '.join(str(phone) for phone in self.phones)}"
        if not self.phones and self.birthday and self.birthday.value.strftime("%d.%m.%Y") != "01.01.0001":
            return f'{self.name}: день народження {self.birthday.strftime("%d.%m.%Y")}'
        return f"У контакта {self.name} не збережено номери телефонів або день народження"


class AddressBook(UserDict):
    def __init__(self, filename="addressbook.json"):
        self.data = UserDict()
        self.filename = filename
        # self.load_data()
    
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        self.save_data()
        
        phones_print = ", ".join(str(phone_print) for phone_print in record.phones)
        if record.birthday and record.phones:
            return f'Я додав контакт "{record.name}" з номером {phones_print} та днем народження {record.birthday.value.strftime("%d.%m.%Y")} до книги контактів'
        if record.birthday and not record.phones:
            return f'Я додав контакт "{record.name}" з днем народження {record.birthday.value.strftime("%d.%m.%Y")} до книги контактів'
        return f'Я додав контакт "{record.name}" з номером {phones_print} до книги контактів'
    
    def open_empty_json(self):
        print("Start open_empty_json function")
        with open(self.filename, 'w', encoding='utf-8') as fb:
            json.dump({}, fb)
    
    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as fb:
                try:
                    data = json.load(fb)
                except:
                    return None
                for name_, record_data in data.items():
                    name = Name(name_)
                    phone = Phone(list(record_data.get('phones'))[0])
                    birthday_ = record_data.get('birthday', "01.01.0001")
                    birthday = Birthday(birthday_)
                    record = Record(name, phone, birthday)
                    for p in record_data.get('phones')[1:]:
                        phone_to_add = Phone(p)
                        record.add_phone(phone_to_add)
                    self.data[name_] = record
        except FileNotFoundError:
            with open(self.filename, 'w') as fb:
                json.dump({}, fb)
    
    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as fb:
            data = {str(name): {
                'phones': [str(phone) for phone in record.phones],
                'birthday': str(record.birthday.value.strftime("%d.%m.%Y")) if record.birthday else "01.01.0001"
            } for name, record in self.data.items()}
            json.dump(data, fb)
    
    def search_info(self, search_query):
        search_results = []
        for key_ab in self.data:
            record_name = str(self.data[key_ab].name)
            if search_query.lower() in record_name.lower():
                search_results.append(f'"{search_query}" знайдено у {record_name}')
                continue
            for phone in self.data[key_ab].phones:
                result_string = ""
                SYMBOLS = ["-", "+", "(", ")"]
                for i in str(phone).lower():
                    if i not in SYMBOLS:
                        result_string += i
                if search_query.lower() in result_string:
                    search_results.append(f'"{search_query}" знайдено у {record_name}: {str(phone).lower()}')
            if search_query in self.data[key_ab].birthday.value.strftime("%d.%m.%Y"):
                search_results.append(f'"{search_query}" знайдено у {record_name}, день народження {self.data[key_ab].birthday.value.strftime("%d.%m.%Y")}')
                continue
        if search_results:
            search_results = '\n'.join(search_results)
            return search_results
        return f'Я не зміг знайти нічого по запиту {search_query}'

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            self.save_data()
            return f'Я видалив запис {name}'
        return f'Я не зміг знайти запис {name}'

    def show_all_contacts(self):
        if self.values():
            return "\n".join(str(r) for r in self.values())
        else:
            return 'Книга контактів пуста'
        
    def __iter__(self, n=1):
        self._index = 0
        self._items = list(self.data.values())
        self._step = n
        return self

    def __next__(self):
        if self._index < len(self._items):
            item = self._items[self._index]
            self._index += self._step
            return item
        else:
            raise StopIteration

    def __str__(self):
        return "\n" + "\n".join(str(record) for record in self.data.values())


# ==============================================
if __name__ == "__main__":
    name_1 = Name("Ivan")
    phone_1 = Phone("+380-50-448-99-99")
    birthday_1 = Birthday("01.01.2000")
    record_1 = Record(name_1, phone_1, birthday_1)
    address_book_1 = AddressBook()
    address_book_1.add_record(record_1)
    
    name_2 = Name("Petro")
    phone_2 = Phone("+380-67-445-99-99")
    phone_3 = Phone("(063)225-11-22")
    phone_4 = Phone("(044)290-00-01")
    birthday_2 = Birthday("01.01.1991")
    record_2 = Record(name_2, phone_2, birthday_2)
    address_book_1.add_record(record_2)
    record_2.add_phone(phone_3)
    record_2.add_phone(phone_4)
    
    name_3 = Name("Helge")
    phone_5 = Phone("673332211")
    phone_6 = Phone("(063)666333444")
    phone_7 = Phone("2909901")
    birthday_3 = Birthday("01.08.1992")
    record_3 = Record(name_3, phone_5, birthday_3)
    address_book_1.add_record(record_3)
    record_3.add_phone(phone_6)
    record_3.add_phone(phone_7)
    
    name_4 = Name("Bill")
    birthday_4 = Birthday("01.08.2023")
    record_4 = Record(name_3, birthday=birthday_3)
    address_book_1.add_record(record_4)
    record_4.del_birthday(birthday_4)
    print("record_4:", record_4)
    
    # print(address_book_1)
    
    counter = 0
    for i in address_book_1:
        print("page #", counter + 1)
        print(i)
        counter += 1