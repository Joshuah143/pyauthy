import pyauthy
import json

users = {'user1': ['pass1', 'email1', 'TOTPkey1'],
         'user2': ['pass1', 'email1', 'TOTPkey1']}


def login():
    user = input('Username:\t')
    try:
        if users[user][0] == input('Password:\t'):
            try:
                codes = users[user][3]
            except KeyError:
                codes = None
            if pyauthy.totp_handler.totp(key=users[user][2], unused_backup_codes=codes).check_otp(input('TOTP key:\t')):
                return True, user
    except KeyError:
        print('INVALID USER')
        raise KeyError
    return False, user


def add_user(users: list):
    totp = pyauthy.totp_handler.totp()
    totp.setup()
    user = input('Username:\t')
    password = input('Password:\t')
    email = input('Email:\t')
    print(f'Your qrcode: {totp.qrcode()}\nYour TOTP key: {totp.key}\nYour backup codes:{totp.backup.unused_codes}')
    users += {user: [password, email, totp.key, totp.backup.unused_codes]}




if __name__ == '__main__':
    question = input('What would you like to do? (login/add user)\t')
    if question == 'login':
        state, user = login()
        if state:
            print(f'Welcome {user}!\nThe secret is: Joshua is awesome')
        else:
            print('LOGIN FAILED')
    elif question == 'add user':
        add_user()
    else:
        print('INVALID USER')