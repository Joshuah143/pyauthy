import base64
import hmac
import smtplib
import twilio.rest as twil
import random
import datetime
import hashlib
from qrcode import make
import time
import os


class Auth:
    def __init__(self,
                 trys=3,
                 digits=6,
                 numsonly=True,
                 sid=os.environ['TwillioSID'],
                 tokensid=os.environ['Twilliotoken'],
                 default_smtp_server="smtp.gmail.com",
                 gmail_user='joshuahimmens@gmail.com',
                 gmail_password=os.environ['gmailpassword'],
                 default_name='Joshua Himmens'):
        self.sid = sid
        self.tokensid = tokensid
        self.trys = trys
        self.digits = digits
        self.numsonly = numsonly
        self.passed = None
        self.carriers = {
            "Bell": "@txt.bell.ca",
            "Solo": "@txt.bell.ca",
            "Chatr": "@pcs.rogers.com",
            "Rogers": "@pcs.rogers.com",
            "Tbaytel": "@pcs.rogers.com",
            "Eastlink": "@txt.eastlink.ca",
            "Fido": "@fido.ca",
            "Koodo": "@msg.koodomobile.com",
            "MTS": "@text.mtsmobility.com",
            "PC": "@mobiletxt.ca",
            "Public": "@msg.telus.com",
            "Sasktel": "@sms.sasktel.com",
            "TELUS": "@msg.telus.com",
            "Virgin": "@vmobile.ca",
            "WIND": "@txt.windmobile.ca"
        }
        self._default_smtp_server = default_smtp_server
        self._gmail_user = gmail_user
        self._gmail_password = gmail_password
        self._default_name = default_name

    def textauth(self, phonenum: str = None, kind=1, car=None):
        self.orginalnum = phonenum
        self._gen_code()
        '''
        kind:
        1 = twilio (requires country code)
        2 = email text (requires number and carrier)
        always give number in full: +1(587)-434-0118
        '''
        if phonenum is None:
            print('YOU NEED TO GIVE NUMBER')
            return False
        if kind == 1:
            phonenum = phonenum.replace('(', '')
            phonenum = phonenum.replace(')', '')
            phonenum = phonenum.replace('-', '')
            self.passed = self.twilliotext(number=phonenum)
        elif kind == 2:
            phonenum = phonenum.replace('(', '')
            phonenum = phonenum.replace(')', '')
            phonenum = phonenum.replace('-', '')
            phonenum = phonenum.replace('+', '')
            if len(phonenum) == 11:
                phonenum = phonenum[1:]
            self.passed = self.email_text_auth(carier=car, number=phonenum)

    def _gen_code(self):
        code = ''
        for _ in range(self.digits):
            if self.numsonly:
                code += str(random.randint(0, 9))
            else:
                num = random.randint(1, 35)
                if num <= 26:
                    if num == 15:
                        code += '0'
                    else:
                        code += str(chr(ord('@') + num))
                else:
                    num -= 26
                    code += str(num)
        self._code = code

    def twilliotext(self, number):
        try:
            print(twil.Client(self.sid,
                              self.tokensid).messages.create(body=self._code,
                                                                       from_='+15873285525',
                                                                       to=number).sid)
            return True
        except Exception as e:
            print(f'FAILED TO SEND TEXT:\n{e}')
            return False

    def email_auth(self, email):
        self._gen_code()
        self.passed = self.sendemail(message=self._code, destination=email)
        # todo: work on making this pretty

    def check_number(self, number='15874340118'):
        nuber = reversed(list(number))
        dns = '.'.join(nuber)
        dns += '.e164.arpa'
        print(dns)
        # todo: work with daniel on VIOP lookup

    def email_text_auth(self, carier, number):
        self._gen_code()
        try:
            app = self.carriers[carier]
        except:
            print('NOT A CARRIER')
            self.passed = False
            return False
        finalemail = number + app
        message = self._code
        self.passed = self.sendemail(message, finalemail)

    def checksend(self):
        if self.passed:
            return True
        else:
            return False

    def sendemail(self, message, destination, standardemail=False):
        server = smtplib.SMTP_SSL(f'{self._default_smtp_server}', 465)
        if standardemail:
            emailintro = "Hi,"
            emailextro = f"Regards,\n{self._default_name}\n\n\n This email was automatically sent with python," \
                         f" if there is any errors please email me back at '{self._gmail_user}'"
            message = f"""Subject: Auth from {self._default_name}
            From: {self._default_name}
            {emailintro}
            {message}
            {emailextro}
            sent at: {datetime.datetime.now()}"""
        try:
            server.login(self._gmail_user, self._gmail_password)
            server.sendmail(self._gmail_user, destination, message)
            server.close()
            print("email sent")
            return True
        except Exception as e:
            print("email failed" + str(e))
            return False

    def check_code(self, checker: str = None):
        if self.trys > 0:
            self.trys -= 1
        else:
            print('LIMIT REACHED')
            return 'LIMIT REACHED'
        if checker is None:
            checker = input('authentication code: ')
        checker = checker.upper()
        checker.replace('O', '0')
        if checker == self._code:
            print('PASSED')
            return True
        else:
            print('FAILED')
            return False

    class TOTP:
        def __init__(self, key: str = 0, issuer='JoshuaH', username='joshua.himmens@icloud.com'):
            if key == 0:
                self.gentotpkey()
            else:
                self.key = key
            self.digits = 6
            self.period = 30
            self.issuer = issuer
            self.user = username
            self.digest = hashlib.sha1


        def getkey(self):
            return self.key

        def genthree(self):
            return [self.generate_otp(-1), self.generate_otp(), self.generate_otp(1)]

        def gentotpkey(self):
            key = ''
            choices = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')
            for _ in range(32):
                key += random.choice(choices)
            print(key)
            self.key = key

        def qrcode(self):
            with open('QR_code.png', 'w'):
                p = make(self.link)
                p.save('test.png')  # save png QR code
            return self.link

        @property
        def link(self):
            return f'otpauth://totp/{self.user}?secret={self.key}&issuer={self.issuer}' \
                   f'&algorithm=SHA1&digits={self.digits}&period={self.period}'

        @property
        def count(self):
            return int(time.mktime(datetime.datetime.now().timetuple()) // self.period)

        def generate_otp(self, offset: int = 0) -> str:
            hasher = hmac.new(self.byte_secret(), self.int_to_bytestring(offset=offset), self.digest)
            hmac_hash = bytearray(hasher.digest())
            offset = hmac_hash[-1] & 0xf
            code = ((hmac_hash[offset] & 0x7f) << 24 |
                    (hmac_hash[offset + 1] & 0xff) << 16 |
                    (hmac_hash[offset + 2] & 0xff) << 8 |
                    (hmac_hash[offset + 3] & 0xff))
            str_code = str(code % 10 ** self.digits)
            while len(str_code) < self.digits:
                    str_code = '0' + str_code
            return str_code

        def byte_secret(self):
            secret = self.key
            missing_padding = len(self.key) % 8
            if missing_padding != 0:
                secret += '=' * (8 - missing_padding)
            return base64.b32decode(secret, casefold=True)

        def int_to_bytestring(self, offset: int = 0, padding: int = 8):
            return (self.count + offset).to_bytes(padding, 'big')


