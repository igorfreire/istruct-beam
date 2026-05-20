class SimpleBeamAnalysis:
    def __init__(self, span_m: float, load_kN_per_m: float):
        self.L = span_m
        self.q = load_kN_per_m

    def calculate(self):
        Mmax = self.q * self.L**2 / 8
        Vmax = self.q * self.L / 2

        return {
            "Mmax_kNm": Mmax,
            "Vmax_kN": Vmax
        }