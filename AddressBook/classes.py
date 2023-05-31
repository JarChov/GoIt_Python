from collections import UserDict
from datetime import datetime
import re
import csv


class WrongName(Exception):
    pass


class WrongPhone(Exception):
    pass


class WrongBd(Exception):
    pass


class Field():
    def __init__(self, value):
        self.__value = None

        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if isinstance(value, str) and len(value) > 2:
            Field.value.fset(self, value)
        else:
            raise WrongName

    def __repr__(self):
        return f'Name: {self.value}'


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        phone_field = re.findall(r'\d', value)
        if len(phone_field) == 10 or len(phone_field) == 12:
            Field.value.fset(self, value)
        else:
            raise WrongPhone

    def __repr__(self):
        return f'Phone:  {self.value}'


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        bd_field = re.findall(r'\d', value)
        if len(bd_field) == 8:
            Field.value.fset(self, value)
        else:
            raise WrongBd

    def __repr__(self):
        return f'Birthday{self.value}'


class Record():

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_phone(self, old_phone_num, new_phone_num):
        for phone_num in self.phones:
            if phone_num.value == old_phone_num.value:
                self.phones.remove(phone_num)
                self.phones.append(new_phone_num)

    def delete_phone(self, phone):
        for phone_num in self.phones:
            if phone_num.value == phone.value:
                self.phones.remove(phone_num)

    def days_to_birthday(self):
        if self.birthday:
            user_bd = datetime.strptime(str(self.birthday).replace('-', ' '), '%d %m %Y')

            if int(datetime.now().month) >= int(user_bd.month) and int(datetime.now().day) > int(user_bd.day):
                user_bd = datetime(datetime.now().year + 1, user_bd.month, user_bd.day)
            elif int(datetime.now().month) == int(user_bd.month) and int(datetime.now().day) == int(user_bd.day):
                return f'0 days'
            else:
                user_bd = datetime(datetime.now().year, user_bd.month, user_bd.day)
            return f'{(user_bd - datetime.now()).days} days'


class ContactsIterable:
    def __init__(self, contacts, N=2):
        self.contacts = contacts
        self.N = N
        self.contacts_counter = 0
        # self.contacts_page = []

    def __next__(self):
        if self.contacts_counter < len(self.contacts):
            contacts_page = self.contacts[self.contacts_counter:min(self.contacts_counter + self.N, len(self.contacts))]
            self.contacts_counter += self.N
            return contacts_page
        raise StopIteration


class AddressBook(UserDict):

    def __iter__(self):
        return ContactsIterable(list(self.data.values()))

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def search(self, input_data):
        search_result = {}
        for k, v in self.data.items():
            # print(k, v.phones)
            for phone in v.phones:
                if input_data in k or input_data in str(phone):
                    search_result[k] = v
        return search_result

    def save_record_to_file(self) -> None:

        with open('user_book.csv', 'w', encoding='utf-8') as ub:
            field_names = ['User name', 'User phone-1', 'User phone-2', 'User birthday']
            writer = csv.DictWriter(ub, fieldnames=field_names)
            writer.writeheader()
            for page in self:
                for contact in page:
                    itphones = iter(contact.phones)

                    data = {
                        'User name': contact.name.value,
                        'User phone-1': next(itphones, None),
                        'User phone-2': next(itphones, None),
                        'User birthday': contact.birthday
                        }
                    writer.writerow(data)

                    # if len(contact.phones) == 1 and contact.birthday:
                    #     writer.writerow({'User name': contact.name.value, 'User phone-1': contact.phones[0],
                    #                  'User phone-2': None, 'User birthday': contact.birthday})
                    # elif len(contact.phones) == 1 and not contact.birthday:
                    #     writer.writerow({'User name': contact.name.value, 'User phone-1': contact.phones[0],
                    #                  'User phone-2': None, 'User birthday': None})
                    # else:
                    #     writer.writerow({'User name': contact.name.value, 'User phone-1': contact.phones[0],
                    #                  'User phone-2': contact.phones[1], 'User birthday': contact.birthday})

    def open_record_from_file(self):
        with open('user_book.csv', 'r') as ub:
            reader = csv.DictReader(ub)
            for row in reader:
                if row['User birthday'] == '':
                    restored_record = Record(Name(row['User name']), Phone(row['User phone-1']))
                else:
                    restored_record = Record(Name(row['User name']), Phone(row['User phone-1']),
                                             Birthday(row['User birthday']))
                if row['User phone-2']:
                    restored_record.add_phone(row['User phone-2'])

                self.add_record(restored_record)
            return self




if __name__ == '__main__':
    # For testing:
    name = Name('some_name')
    name_1 = Name('some_name_1')
    name_2 = Name('some_name_2')
    phone_1 = Phone('380631234567')
    phone_2 = Phone('0639876543')
    phone_3 = Phone('0333111111')
    birthday = Birthday('15-05-2000')


    # Creating a record
    record_1 = Record(name, phone_1, birthday)
    record_2 = Record(name_1, phone_1, birthday)
    record_3 = Record(name_2, phone_3, birthday)
    # print(record_1)

    # Method add_phone
    record_1.add_phone(phone_2)
    record_1.add_phone(phone_3)
    # print(record_1.phones)
    # for phone in record_1.phones:
    #     print(phone)

    # Method delete_phone
    record_1.delete_phone(phone_2)
    # print(record_1.phones)

    # Method change_phone
    record_1.change_phone(phone_1, Phone('0675555555'))
    # print(record_1.phones)

    # Method days to birthday
    # print(record_1.days_to_birthday())

    # Method update dict
    user_dict = AddressBook()
    user_dict.add_record(record_1)
    user_dict.add_record(record_2)
    user_dict.add_record(record_3)
    # print(user_dict.data)
    record = user_dict.data.get(name.value)

    # Find method
    new_user_dict = AddressBook()
    new_user_dict.open_record_from_file()
    find_data = '123'

    find_dict = new_user_dict.search(find_data)
    print(find_dict)


    # user_dict.save_record_to_file()
    # print(f'user_dist: {user_dict}')
    # print(ContactsIterable(list(user_dict), 5).__next__())
    # user_dict_saved = AddressBook()
    # user_dict_saved = AddressBook.open_record_from_file
    # print(user_dict_saved)

