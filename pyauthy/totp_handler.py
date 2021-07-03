import binascii
import hashlib
import random
import time
import hmac
import datetime
from qrcode import make
from base64 import b32decode
from pyauthy import backupcodes


class totp:
    def __init__(self,
                 key: str = 0,
                 issuer: str = 'JoshuaH',
                 username: str = 'joshua.himmens@icloud.com',
                 used_backup_codes: list = None,
                 unused_backup_codes: list = None):
        """
        :param key:
        :param issuer:
        :param username:
        :param used_backup_codes:
        :param unused_backup_codes:
        """
        if key == 0:
            self.gentotpkey()
        else:
            self.key = key
        self.digits = 6
        self.period = 30
        self.issuer = issuer
        self.user = username
        self.digest = hashlib.sha1
        self.backup = backupcodes(unused_backup_codes, used_backup_codes)

    def check_otp(self, given: str or int) -> bool:
        """
        :param given:
        :return:
        """
        given = str(given)
        if given in self.genthree:
            return True
        elif self.backup.check_code(given):
            return True
        else:
            return False

    def setup(self) -> list[str, list[str]]:
        # todo: Fix this thing
        return [self.key, self.backup.unused_codes]

    @property
    def getkey(self) -> str:
        """
        :return:
        """
        return self.key

    @property
    def genthree(self) -> list:
        """
        :return:
        """
        return [self.generate_otp(-1), self.generate_otp(), self.generate_otp(1)]

    def gentotpkey(self):
        """
        :return: returns the TOTP key AKA the secret
        """
        choices = list('234567ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        key = ''.join(random.choice(choices) for _ in range(32))
        self.key = key
        return self.key

    def qrcode(self, filename: str = 'QR_code.png') -> str:
        """
        :return:
        """
        if not filename.endswith('.png'):
            filename += '.png'
        p = make(self.link)
        p.save(filename)  # save png QR code
        return self.link

    @property
    def link(self) -> str:
        """
        :return:
        """
        return f'otpauth://totp/{self.user}?secret={self.key}&issuer={self.issuer}' \
               f'&algorithm=SHA1&digits={self.digits}&period={self.period}'

    @property
    def count(self) -> int:
        """
        :return:
        """
        return int(time.mktime(datetime.datetime.now().timetuple()) // self.period)

    def generate_otp(self, offset: int = 0) -> str:
        """
        :param offset:
        :return:
        """
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
        """
        :return:
        """
        secret = self.key
        missing_padding = len(self.key) % 8
        if missing_padding != 0:
            secret += '=' * (8 - missing_padding)
        try:
            return b32decode(secret, casefold=True)
        except binascii.Error:
            raise KeyError

    def int_to_bytestring(self, offset: int = 0, padding: int = 8) -> bytes:
        """
        :param offset: the offset argument changes what the count will be used when calculating the TOTP code.
         for example if you set it to one it will find the next code and -1 will find the last one; no matter
         what the period of each code is
        :param padding: determines the total number of bytes that are returned
        :return: returns the byte representation of the count plus the offset
        """
        return (self.count + offset).to_bytes(padding, 'big')
