import random


class BackupCodes:
    def __init__(self, unused_codes: list = None, used_codes: list = None):
        if used_codes is None:
            self.used_codes = []
        else:
            self.used_codes = list(used_codes)
        if unused_codes is None:
            self.unused_codes = []
        else:
            self.unused_codes = list(unused_codes)

    def gencodes(self, number_of_codes: int = 6,
                 code_length: int = 8,
                 nums: bool = True,
                 alpha: bool = False) -> list:
        if (not nums) and (not alpha):
            raise Exception
        pool = []
        code_list = []
        if nums:
            pool += list('1234567890')
        if alpha:
            pool += list('qwertyuiopasdfghjklzxcvbnm')
        for _ in range(number_of_codes):
            _code = ''
            for _ in range(code_length):
                _code += str(random.choice(pool))
            code_list.append(_code)
        self.unused_codes = [code_list]
        self.unused_codes = []
        return code_list

    def check_code(self, given: int or str, strict: bool = True) -> bool:
        given = str(given)
        if given in self.unused_codes:
            self.unused_codes.pop(self.unused_codes.index(given))
            self.used_codes += given
        elif given in self.unused_codes:
            if strict:
                return False
            elif not strict:
                return True
        return False

