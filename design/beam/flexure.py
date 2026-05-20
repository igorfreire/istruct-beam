import math


class BeamFlexure:

    def __init__(self, section, concrete, steel, Md_kNm: float):

        self.section = section
        self.concrete = concrete
        self.steel = steel

        self.Md = Md_kNm

    def calculate(self):

        # ==================================================
        # GEOMETRIA
        # ==================================================

        bw = self.section.bw / 100  # m
        d = self.section.d / 100    # m

        # ==================================================
        # MATERIAIS
        # ==================================================

        fcd = self.concrete.fcd * 1e6
        fyd = self.steel.fyd * 1e6

        # ==================================================
        # MOMENTO
        # ==================================================

        Md = self.Md * 1e3  # kN.m -> N.m

        # ==================================================
        # CÁLCULO DA LINHA NEUTRA
        # ==================================================

        A = 0.68 * fcd * bw

        discriminant = (A * d) ** 2 - 1.36 * fcd * bw * Md

        if discriminant <= 0:

            return {
                "error": True,
                "message": "Momento excessivo para a seção",
                "suggestion": "Aumentar altura da viga"
            }

        x = (
            A * d -
            math.sqrt(discriminant)
        ) / A

        # ==================================================
        # VERIFICAÇÃO DE DOMÍNIO
        # ==================================================

        x_lim = 0.45 * d

        if x > x_lim:

            return {
                "error": True,
                "message": "Seção ultrapassou domínio permitido",

                "x_m": x,
                "x_lim_m": x_lim,

                "suggestion": (
                    "Aumentar seção "
                    "ou implementar dupla armadura"
                )
            }

        # ==================================================
        # BRAÇO DE ALAVANCA
        # ==================================================

        z = d - 0.4 * x

        # ==================================================
        # ÁREA DE AÇO
        # ==================================================

        As_calc = Md / (z * fyd)

        # ==================================================
        # ARMADURA MÍNIMA
        # ==================================================

        As_min_cm2 = (
            0.0015 *
            self.section.bw *
            self.section.h
        )

        As_min = As_min_cm2 / 1e4

        As_final = max(
            As_calc,
            As_min
        )

        # ==================================================
        # TAXA DE ARMADURA
        # ==================================================

        rho = As_final / (bw * d)

        # ==================================================
        # TAXA MÁXIMA
        # ==================================================

        rho_max = 0.04

        if rho > rho_max:

            return {
                "error": True,
                "message": "Taxa de armadura excessiva",

                "rho": rho,
                "rho_max": rho_max,

                "suggestion": (
                    "Aumentar seção "
                    "ou usar dupla armadura"
                )
            }

        # ==================================================
        # RESULTADO FINAL
        # ==================================================

        return {

            "error": False,

            "As_cm2": As_final * 1e4,
            "As_calc_cm2": As_calc * 1e4,
            "As_min_cm2": As_min_cm2,

            "x_m": x,
            "x_lim_m": x_lim,

            "z_m": z,
            "d_m": d,

            "rho": rho,
            "rho_max": rho_max
        }