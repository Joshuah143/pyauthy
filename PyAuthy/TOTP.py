import hashlib
import random
import time
import hmac
import datetime
from qrcode import make
from base64 import b32decode
import Backupcodes


class TOTP:
    def __init__(self,
                 key: str = 0,
                 issuer: str = 'JoshuaH',
                 username: str = 'joshua.himmens@icloud.com',
                 used_backup_codes: list = None,
                 unused_backup_codes: list = None):
        if key == 0:
            self.gentotpkey()
        else:
            self.key = key
        self.digits = 6
        self.period = 30
        self.issuer = issuer
        self.user = username
        self.digest = hashlib.sha1
        self.backup = Backupcodes.BackupCodes(unused_backup_codes, used_backup_codes)

    def check_otp(self, given: str or int) -> bool:
        given = str(given)
        if given in self.genthree:
            return True
        elif self.backup.check_code(given):
            return True
        else:
            return False

    def setup(self) -> list[str, list[str]]:

        return [self.key, self.backup.unused_codes]

    @property
    def getkey(self) -> str:
        return self.key

    @property
    def genthree(self) -> list:
        return [self.generate_otp(-1), self.generate_otp(), self.generate_otp(1)]

    def gentotpkey(self):
        key = ''
        choices = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')
        for _ in range(32):
            key += random.choice(choices)
        print(key)
        self.key = key

    def qrcode(self) -> str:
        with open('QR_code.png', 'w'):
            p = make(self.link)
            p.save('test.png')  # save png QR code
        return self.link

    @property
    def link(self) -> str:
        return f'otpauth://totp/{self.user}?secret={self.key}&issuer={self.issuer}' \
               f'&algorithm=SHA1&digits={self.digits}&period={self.period}'

    @property
    def count(self) -> int:
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
        return b32decode(secret, casefold=True)

    def int_to_bytestring(self, offset: int = 0, padding: int = 8) -> bytes:
        return (self.count + offset).to_bytes(padding, 'big')