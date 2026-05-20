import math


AVAILABLE_BARS = {
    6.3: 0.31,
    8.0: 0.50,
    10.0: 0.79,
    12.5: 1.23,
    16.0: 2.01,
    20.0: 3.14
}


MIN_BARS = 2  # 🔹 regra construtiva


def choose_bars(As_required_cm2):
    solutions = []

    for diameter, area in AVAILABLE_BARS.items():
        n_bars = math.ceil(As_required_cm2 / area)

        # 🔹 garantir mínimo construtivo
        n_bars = max(n_bars, MIN_BARS)

        As_provided = n_bars * area

        solutions.append({
            "diameter_mm": diameter,
            "n_bars": n_bars,
            "As_provided": As_provided
        })

    # 🔹 critério melhorado:
    # 1. menor número de barras
    # 2. menor excesso de aço
    best = min(
        solutions,
        key=lambda x: (x["n_bars"], x["As_provided"])
    )

    return best