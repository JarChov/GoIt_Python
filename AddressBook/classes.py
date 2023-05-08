from collections import UserDict


class Field():
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record():

    def __init__(self, name, phone=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_phone(self, old_phone_num, new_phone_num):
        for phone_num in self.phones:
            if phone_num.value == old_phone_num.value:
                self.phones.remove(phone_num)
                self.phones.append(new_phone_num)

        # if old_phone_num in self.phones:
        #     self.phones.remove(old_phone_num)
        #     self.phones.append(new_phone_num)

    def delete_phone(self, phone):
        for phone_num in self.phones:
            if phone_num.value == phone.value:
                self.phones.remove(phone_num)
        # if phone in self.phones:
        #     self.phones.remove(phone)


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record


if __name__ == '__main__':
    # For testing:
    name = Name('Some_name')
    phone_1 = Phone('380631234567')
    phone_2 = Phone('0639876543')
    phone_3 = Phone('0333')
    # print(phone_1, phone_2)

    # Creating a record
    record_1 = Record(name, phone_1)
    print(record_1)

    # Method add_phone
    record_1.add_phone(phone_2)
    record_1.add_phone(phone_3)
    print(record_1.phones)

    # Method delete_phone
    record_1.delete_phone(phone_2)
    print(record_1.phones)

    # Method change_phone
    record_1.change_phone(phone_1, Phone('06755555555'))
    print(record_1.phones)

    # Method update dict
    user_dict = AddressBook()
    user_dict.add_record(record_1)
    # print(user_dict.data)
    record = user_dict.data.get(name.value)
    print(record.phones)

