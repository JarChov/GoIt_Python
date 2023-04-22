from datetime import datetime


days_name = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}


def get_birthdays_per_week(users: list):
    current_year = datetime.now().year
    holiday = (0, 6)
    invitation_list = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': []
    }
    for user in users:
        for k, v in user.items():
            v = v.replace('-', ' ')
            user_bd = datetime.strptime(v, '%d %m %Y')
            user_bd = datetime(current_year, user_bd.month, user_bd.day)

            if int(user_bd.strftime('%W')) == int(datetime.now().strftime('%W')) + 1 and \
                    int(user_bd.strftime('%w')) not in holiday:
                d_name = days_name.get(user_bd.weekday())
                invitation_list[d_name].append(k)
            elif int(user_bd.strftime('%W')) == int(datetime.now().strftime('%W')) and \
                int(user_bd.strftime('%w')) in holiday:
                invitation_list['Monday'].append(k)

    for k, v in invitation_list.items():
        if v:
            user = ','.join(v)
            print(f'{k}: {user}')


users = [{'Jan': '25-04-1990'}, {'Pedro': '28-04-1990'}, {'Hose': '23-04-1990'}, {'Pavlo': '22-04-1990'}]

get_birthdays_per_week(users)
