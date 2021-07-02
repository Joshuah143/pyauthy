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

    @property
    def getkey(self):
        return self.key

    @property
    def genthree(self):
        return [self.generate_otp(-1), self.generate_otp(), self.generate_otp(1)]

    def gentotpkey(self):
        key = ''
        choices = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')
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
        return b32decode(secret, casefold=True)

    def int_to_bytestring(self, offset: int = 0, padding: int = 8):
        return (self.count + offset).to_bytes(padding, 'big')