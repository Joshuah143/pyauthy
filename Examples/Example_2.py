from pyauthy.authy_base import two_factor


def verify_phone(phone_number: str) -> bool:
    twofa = two_factor()
    twofa.text_auth(phone_number)
    if twofa.check_code(input('2FA code:')):
        print('AUTHENTICATION SUCCESSFUL')
        return True
    else:
        print('AUTHENTICATION FAILED')
        return False


if __name__ == '__main__':
    number = input('phone number:')
    if verify_phone(number):
        print('Thanks for verifying your number!')
