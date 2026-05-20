import math


class BeamShear:
    def __init__(self, section, concrete, steel, Vd_kN: float):
        self.section = section
        self.concrete = concrete
        self.steel = steel
        self.Vd = Vd_kN

    def calculate(self):
        bw = self.section.bw / 100  # m
        d = self.section.d / 100    # m

        fck = self.concrete.fck
        fyd = self.steel.fyd * 1e6

        Vd = self.Vd * 1e3  # N

        # ==================================================
        # Vrd2 — compressão diagonal do concreto
        # ==================================================

        alpha_v2 = 1 - (fck / 250)

        fcd = self.concrete.fcd * 1e6

        Vrd2 = 0.27 * alpha_v2 * fcd * bw * d

        if Vd > Vrd2:
            return {
                "error": True,
                "message": "Viga falhou em Vrd2 (compressão diagonal)",
                "Vd_kN": Vd / 1e3,
                "Vrd2_kN": Vrd2 / 1e3,
                "suggestion": "Aumentar seção da viga"
            }

        # ==================================================
        # Parcela resistente do concreto
        # ==================================================

        Vc = 0.6 * (fck ** (2/3)) * bw * d * 1e6

        # ==================================================
        # Estribo mínimo
        # ==================================================

        phi = 5.0
        area_bar = 0.196  # cm²
        Asw = 2 * area_bar

        z = 0.9 * d

        # ==================================================
        # Caso 1 — concreto resiste sozinho
        # ==================================================

        if Vd <= Vc:

            s_max = min(0.6 * d * 100, 30)

            return {
                "error": False,
                "Vc_kN": Vc / 1e3,
                "Vs_kN": 0,
                "Vrd2_kN": Vrd2 / 1e3,
                "spacing_cm": s_max,
                "phi_mm": phi,
                "is_minimum_stirrup": True
            }

        # ==================================================
        # Caso 2 — precisa armadura transversal
        # ==================================================

        Vs = Vd - Vc

        s = (Asw / 1e4) * fyd * z / Vs

        s_cm = s * 100

        # Limites normativos simplificados
        s_max = min(0.6 * d * 100, 30)

        s_final = min(s_cm, s_max)

        return {
            "error": False,
            "Vc_kN": Vc / 1e3,
            "Vs_kN": Vs / 1e3,
            "Vrd2_kN": Vrd2 / 1e3,
            "spacing_cm": s_final,
            "spacing_calc_cm": s_cm,
            "phi_mm": phi,
            "is_minimum_stirrup": False
        }