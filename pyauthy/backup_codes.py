import random


class backupcodes:
    def __init__(self,
                 unused_codes: list = None,
                 used_codes: list = None):
        """
        :param unused_codes: this argument is a list of any unused codes that are still valid for use
        :param used_codes:  specifies a list of previously used codes that are only valid if the
        authentication type is not strict, mostly just here for development use
        """
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
                 alpha: bool = False) -> list[str]:
        """
        :param number_of_codes: the number of 2FA backup codes to be generated
        :param code_length: length of each individual code
        :param nums: if numbers should be in the codes
        :param alpha: if there chould be letters in the codes
        :return: a list of strings that are the backup codes
        """
        if (not nums) and (not alpha):
            raise NotImplementedError
        pool = []
        if nums:
            pool += list('1234567890')
        if alpha:
            pool += list('qwertyuiopasdfghjklzxcvbnm')
        code_list = [''.join(random.choice(pool) for _ in range(code_length)) for _ in range(number_of_codes)]
        self.unused_codes = code_list
        self.used_codes = []
        return code_list

    def check_code(self, given: int or str, strict: bool = True) -> bool:
        """
        :param given: the code that is checked against the real codes and backups
        :param strict: if old backup codes will be accepted
        :return: return weather or not the 2FA method was a success so if the code was wrong it will return false
        """
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

