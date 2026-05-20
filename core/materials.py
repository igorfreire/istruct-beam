class Concrete:
    def __init__(self, fck_mpa: float):
        self.fck = fck_mpa
        self.gamma_c = 1.4
        self.fcd = fck_mpa / self.gamma_c


class Steel:
    def __init__(self, fyk_mpa: float = 500):
        self.fyk = fyk_mpa
        self.gamma_s = 1.15
        self.fyd = fyk_mpa / self.gamma_s