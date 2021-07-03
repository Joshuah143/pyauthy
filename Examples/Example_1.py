import pyauthy
import json

usersexample = {
    'user1': ['pass1', 'email1', 'EXAMPLETOTPKEYEXAMPLETOTPKEYII'],
    'user2': ['pass1', 'email1', 'EXAMPLETOTPKEYEXAMPLETOTPKEYII']}


def login(users):
    user = input('Username:')
    if user in users:
        if users[user][0] == input('Password:'):
            try:
                codes = users[user][3]
            except IndexError:
                codes = None
            try:
                if pyauthy.totp_handler.totp(key=users[user][2], unused_backup_codes=codes).check_otp(input('TOTP key:')):
                    return True, user
            except KeyError:
                print('INVALID TOTP KEY')
        else:
            print('INCORRECT PASSWORD')
    else:
        print('INVALID USER')
    return False, user


def add_user(users: list):
    totp = pyauthy.totp_handler.totp()
    totp.setup()
    user = input('Username:\t')
    password = input('Password:\t')
    email = input('Email:\t')
    print(f'Your link: {totp.qrcode("Example_QR_code.png")} '
          f'(image available in file)\nYour TOTP key: {totp.key}'
          f'\nYour backup codes:{totp.backup.unused_codes}')
    addition = {user: [password, email, totp.key, totp.backup.unused_codes]}
    print('USER CREATED SUCCESSFULLY')
    return {**users, **addition}


def load_users():
    with open('Example_1_data.json', 'r') as file:
        return json.load(file)


def save_users(users: dict):
    with open('Example_1_data.json', 'w') as file:
        json.dump(users, file, indent='\t')


if __name__ == '__main__':
    users = load_users()
    question = input('What would you like to do? (login/add user)\t')
    if question == 'login':
        state, user = login(users)
        if state:
            print(f'Welcome {user}!\nThe secret is: Joshua is awesome')
        else:
            print('LOGIN FAILED')
    elif question == 'add user':
        users = add_user(users)
    else:
        print('INVALID USER')
    save_users(users)
