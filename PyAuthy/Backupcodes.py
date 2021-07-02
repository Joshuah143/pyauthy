import random


class BackupCodes:
    def __init__(self, used_codes: list = (), unused_codes: list = ()):
        if type(used_codes) == tuple:
            self.used_codes = []
        else:
            self.used_codes = list(used_codes)
        if type(unused_codes) == tuple:
            self.unused_codes = []
        else:
            self.unused_codes = list(unused_codes)

    def gencodes(self, number_of_codes: int = 6,
                 code_length: int = 8,
                 nums: bool = True,
                 alpha: bool = False):
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
        self.used_codes = []


