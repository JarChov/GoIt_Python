from classes import *


# Перевірка чи файл адресної книги існує
try:
    file = open('user_book.csv')
except IOError:
    users = AddressBook()
else:
    users = AddressBook()
    users.open_record_from_file()


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except WrongName:
            return 'User name should be at least 2 letter'
        except WrongPhone:
            return 'User phone number should be at format +380xxxxxxx'
        except KeyError:
            return 'Enter user name'
        except (TypeError, ValueError):
            return 'Give me name and phone or birthday please'
        except IndexError:
            return 'Enter user name'

    return wrapper


def exit_func():
    return


def greetings():
    return 'How can I help you?'


@input_error
def user_adding(user_name, user_phone):
    user_name = Name(user_name)
    user_phone = Phone(user_phone)
    if user_name.value in users.data:
        record = users.pop(user_name.value)
        record.add_phone(user_phone)
        users.add_record(record)
        # users.save_record_to_file(record)
        return f'For user {user_name} added new phone number {user_phone}'
    else:
        record = Record(user_name, user_phone)
        users.add_record(record)
        # users.save_record_to_file(record)
        return f'User {user_name} with number {user_phone} successfully added'


@input_error
def phone_changing(user_name, user_phone_new):
    user_name = Name(user_name)
    user_phone_new = Phone(user_phone_new)
    phones_num = ''

    if user_name.value in users.data:
        record = users.pop(user_name.value)

        if len(record.phones) == 1:
            record.change_phone(record.phones[0], user_phone_new)
            users.add_record(record)
            return f'For user {user_name} number {record.phones[0]} ' \
                   f'successfully changed to new number {user_phone_new}'
        else:
            for phone in record.phones:
                phones_num += str(phone) + '; '
            print(f"User {user_name.value} have phone number's: {phones_num.removesuffix('; ')}")
            user_phone_old = Phone(input(f'Write number should be changed >>> '))
            record.change_phone(user_phone_old, user_phone_new)
            users.add_record(record)

            return f'For user {user_name} number {user_phone_old} ' \
                   f'successfully changed to new number {user_phone_new}'


@input_error
def delete(user_name, user_phone):
    user_name = Name(user_name)
    user_phone = Phone(user_phone)
    if user_name.value in users.data:
        record = users.pop(user_name.value)

        record.delete_phone(user_phone)
        users.add_record(record)
        return f'For user {user_name.value} phone number {user_phone} successfully deleted'


@input_error
def phone_shower(user_name):
    user_name = Name(user_name)
    phones_num = ''
    user_phone = users.get(user_name.value)

    if len(user_phone.phones) == 1:
        return f"User {user_name.value} have phone number: {user_phone.phones[0]}"
    elif len(user_phone.phones) == 0:
        return f"User {user_name.value} haven't phone number"
    else:
        for phone in user_phone.phones:
            phones_num += str(phone) + '; '
        return f"User {user_name.value} have phone number's: {phones_num.removesuffix('; ')}"


def show_all():
    all_user = ''
    phones_num = ''
    # page_counter = 0

    for book_page in users:
        # page_counter += 1
        for records in book_page:
            if len(records.phones) == 1:
                all_user += f'User {records.name} phone number: {records.phones[0]} birthday {records.birthday}\n'
            else:
                for phone in records.phones:
                    phones_num += str(phone) + '; '
                all_user += f"User {records.name} phone number's: {phones_num.removesuffix('; ')}" \
                            f" birthday {records.birthday}\n"
    return all_user


@input_error
def add_birthday(user_name, birthday_date):
    user_name = Name(user_name)
    birthday_date = Birthday(birthday_date)
    if user_name.value in users.data:
        record = users.pop(user_name.value)
        record.birthday = birthday_date
        users.add_record(record)
        return f'For user {user_name} added birthday date {birthday_date}'


def days_to_bd(user_name):
    user_name = Name(user_name)
    if user_name.value in users.data:
        return f'For birthday of user {user_name.value} left {users.data.get(user_name.value).days_to_birthday()}'


def finder(user_data: str):
    founded_data = users.search(user_data)
    all_user = ''
    phones_num = ''
    for records in founded_data.values():
        if len(records.phones) == 1:
            all_user += f'User {records.name} phone number: {records.phones[0]} birthday {records.birthday}\n'
        else:
            for phone in records.phones:
                phones_num += str(phone) + '; '
            all_user += f"User {records.name} phone number's: {phones_num.removesuffix('; ')}" \
                        f" birthday {records.birthday}\n"

    return all_user


COMMANDS = {
    'hello': greetings,
    'add': user_adding,
    'change': phone_changing,
    'phone': phone_shower,
    'show all': show_all,
    'delete': delete,
    'birthday add': add_birthday,
    'birthday left': days_to_bd,
    'find': finder,
    'good bye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    '.': exit_func
}


def command_parser(input_value):
    command, *args = input_value.split()
    try:
        handler = COMMANDS[command.lower()]

    except KeyError:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
            handler = COMMANDS.get(command.lower())
    finally:
        user_phone_old = None
        if len(args) >= 2:
            user_name, user_phone = args[0], args[1]
        elif len(args) == 1:
            user_name = args[0]
            user_phone = None
        else:
            handler = COMMANDS[command.lower()]
            user_name = None
            user_phone = None
        return handler, user_name, user_phone


def main():
    while True:
        handler, user_name, user_data, *args = command_parser(input(f'Enter a command please: '))

        # name = Name(user_name)
        # phone = Phone(user_data) or Birthday(user_data)

        if not user_name and not user_data:
            result = handler()
        elif not user_data:
            result = handler(user_name)
        else:
            result = handler(user_name, user_data)

        if not result:
            print('Good bye!')
            users.save_record_to_file()
            # print(users)
            break
        print(result)


if __name__ == '__main__':
    main()



