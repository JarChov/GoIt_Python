users = {}


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return 'Enter user name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'
    return wrapper


def exit_func(_):
    return


def greetings(_):
    return 'How can I help you?'


@input_error
def user_adding(args):
    user_name, user_phone = args
    users[user_name] = user_phone
    return f'User {user_name} with number {user_phone} successfully added'


@input_error
def phone_changing(args):
    user_name, user_phone = args
    if user_name in users.keys():
        users[user_name] = user_phone
    return f'For user {user_name} number successfully changed to {user_phone}'


@input_error
def phone_shower(args):
    user_name, *args = args
    return f'User {user_name} have phone number: {users[user_name]}'


def show_all(_):
    all_user = ''
    for k, v in users.items():
        all_user += f'User {k} phone number: {v}\n'
    return all_user

COMMANDS = {
    'hello': greetings,
    'add': user_adding,
    'change': phone_changing,
    'phone': phone_shower,
    'show all': show_all,
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
    return handler, args


def main():
    while True:
        handler, *args = command_parser(input(f'Enter a command please: '))
        result = handler(*args)
        if not result:
            print('Good bye!')
            break
        print(result)


if __name__ == '__main__':
    main()



