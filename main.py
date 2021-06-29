import base64
import hmac
import smtplib
from typing import Optional, Any

import twilio.rest as twil
import random
import json
import datetime
import hashlib
from qrcode import make
import time


class Auth:
    def __init__(self,
                 trys=3,
                 digits=6,
                 numsonly=True,
                 sid="ACee46d15aee42ece35152b01a0cf0db61",
                 tokensid='a16dc9df73edf829357d5354e5802147',
                 default_smtp_server="smtp.gmail.com",
                 gmail_user='joshuahimmens@gmail.com',
                 gmail_password='mmslnuunnmvhvomt',
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

    def emailaith(self):
        pass

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
            print(twil.Client(self.sid, self.tokensid).messages.create(body=self._code,
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
            emailextro = f"Regards,\n{self._default_name}\n\n\n This email was automatically sent with python, if there is any errors please email me back at '{self._gmail_user}'"
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

    class TOTP:
        def __init__(self, issuer='JoshuaH', key=0, username='joshua.himmens@icloud.com'):
            if key == 0:
                self.gentotpkey()
            else:
                self.key = key
            self.digits = 6
            self.period = 30
            self.issuer = issuer
            self.user = username
            self.count = int(time.time() // 30)

        def totpnow(self):
            hasher = hmac.new(base64.b32decode(self.key, casefold=True), self.int_to_bytestring(),
                              hashlib.sha1)
            print(bytearray(hasher.digest()))
            print('key', self.key)
            print('haserh', hasher)
            code = (hasher % 10) ** self.digits
            print('FUCK YEAH')

        def generate_otp(self) -> str:
            """
            :param input: the HMAC counter value to use as the OTP input.
                Usually either the counter, or the computed integer based on the Unix timestamp
            """
            input = self.count
            if input < 0:
                raise ValueError('input must be positive integer')
            hasher = hmac.new(self.byte_secret(), self.int_to_bytestring(input), hashlib.sha1)
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

        def byte_secret(self) -> bytes:
            secret = self.key
            missing_padding = len(self.key) % 8
            if missing_padding != 0:
                secret += '=' * (8 - missing_padding)
            return base64.b32decode(secret, casefold=True)

        def gentotpkey(self):
            key = ''
            choices = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')
            for _ in range(32):
                key += random.choice(choices)
            print(key)
            self.key = key

        def qrcode(self):
            'otpauth://totp/JOSHUAH:john.doe@email.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=JOSHUAH&algorithm=SHA1&digits=6&period=30'
            '''mylink = 'otpauth://totp/'  # adds totp label 
            mylink += f'{self.user}'  # suername
            mylink += '?secret='
            mylink += f'{self.key}'  # the key to originate it (SHA1 Hash)
            mylink += '&issuer='
            mylink += f'{self.issuer}'  # issueragain
            mylink += '&algorithm='
            mylink += 'SHA1'  # algorith used, just use fucknng SHA 1 to make life easy
            mylink += '&digits='
            mylink += f'{self.digits}'  # length of totp challange
            mylink += '&period='
            mylink += f'{self.period}'  # length of valid time for TOTP token''' #todo: clean this shit up
            mylink = f'otpauth://totp/{self.user}&issuer={self.issuer}&algorithm=SHA1&digits={self.digits}&period={self.period}'
            self.link = mylink
            with open('QR_code.png', 'w'):
                p = make(mylink)
                p.save('test.png')  # save png QR code
            return mylink, self.key

        def int_to_bytestring(self, padding: int = 8) -> bytes:
            _i = self.count
            """
            Turns an integer to the OATH specified
            bytestring, which is fed to the HMAC
            along with the secret
            """
            result = bytearray()
            while _i != 0:
                result.append(_i & 0xFF)
                _i >>= 8
            return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

        def getkey(self):
            return self.key

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


if False:
    test = Auth()
    test.textauth('+1(587)-434-0118')
    test.check_code()

if False:
    test = Auth()
    test.textauth(kind=2, phonenum='+1(587)-434-0118', car='Bell')
    test.check_code()

if 1:
    test = Auth.TOTP(key='5THY2U2POIFIJQMLSGQER5ZBONFLHTAJ')
    #test.totpnow()
    print(test.generate_otp())
    print(test.qrcode())

if 0:
    test = Auth()
    check = test.check_number()

if 0:
    test = Auth()
    test.email_auth('joshua.himmens@icloud.com')
    check = test.check_number()


#print(hashlib.sha1(str('this is a test').encode()))
#print(hashlib.sha1((176).to_bytes(32, 'little')).digest())

tracking_number = 280697270107
number_to_call = 18004633339
ama_guy = 4033831565
