import os
import random
import smtplib
import datetime
import twilio.rest as twil


class TwoFA:
    def __init__(self,
                 trys=3,
                 digits=6,
                 numsonly=True,
                 sid=1, #os.environ['TwillioSID'],
                 tokensid=1, #os.environ['Twilliotoken'],
                 default_smtp_server="smtp.gmail.com",
                 gmail_user='joshuahimmens@gmail.com',
                 gmail_password= 1,#os.environ['gmailpassword'],
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

    def textauth(self, phonenum: str = None, kind=1, car=None) -> bool:
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
        return True

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

    def twilliotext(self, number) -> bool:
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

    def email_text_auth(self, carier, number) -> bool:
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
        return True

    def checksend(self) -> bool:
        if self.passed:
            return True
        else:
            return False

    def sendemail(self, message, destination, standardemail=False) -> bool:
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

    def check_code(self, checker: str = None) -> bool:
        if self.trys > 0:
            self.trys -= 1
        else:
            print('LIMIT REACHED')
            raise NotImplementedError
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