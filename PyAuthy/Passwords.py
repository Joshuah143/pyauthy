    class Passwords:
        def __init__(self, password: str = ''):
            self.password = password

        def passwordcheck(self, password:str=None):
            if password is None:
                password = self.password
            password_score = 0
            possbile = 0
            checkfor = ['QWERTYUIOPASDFGHJKLZXCVBNM',
                        'qwertyuioplkjhgfdsazxcvbnm',
                        '1234567890',
                        '!@#$%^&*()-_`~][{}\\|:;"\',.<>/?']
            for currentcheck in checkfor:
                if self.checkanyin(password, list(currentcheck)):
                    password_score += 2
                    possbile += 2
                else:
                    possbile += 2
            incremnts = [0, 5, 10, 15, 25, 30]
            for i in incremnts:
                if len(password) >= i:
                    possbile += 1
                    password_score += 1
                else:
                    possbile += 1
            return password_score/possbile

        @staticmethod
        def checkanyin(origin: str, checklist: list):
            for i in checklist:
                if i in origin:
                    return True
            return False

        def passwordgen(self,
                        length: int = 30,
                        ambigous: bool = False,
                        numbers: bool = True,
                        capsletters: bool = True,
                        specialcharters: bool = True,
                        lowercase: bool = True):
            pool = []
            if numbers:
                pool += (list('1234567890'))
            if capsletters:
                pool += (list('QWERTYUIOPASDFGHJKLZXCVBNM'))
            if lowercase:
                pool += (list('qwertyuioplkjhgfdsazxcvbnm'))
            if specialcharters:
                pool += (list('!@#$%^&*()-_`~][{}\\|:;"\',.<>/?'))
            if ambigous:
                pass
            _result = ''
            for _ in range(length):
                _result += str(random.choice(pool))
            self.password = _result
            return _result