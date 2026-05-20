def generate_beam_report(data: dict):

    stirrup_type = (

        "Estribo mínimo"

        if data["minimum_stirrup"]

        else "Estribo calculado"
    )

    report = f"""
===== RELATÓRIO DE DIMENSIONAMENTO DE VIGA =====

---------------- FLEXÃO ----------------

Momento de cálculo:
Md = {data['Md']:.2f} kN.m

Altura útil:
d = {data['d']:.3f} m

Linha neutra:
x = {data['x']:.3f} m

Limite da linha neutra:
x_lim = {data['x_lim']:.3f} m

Braço de alavanca:
z = {data['z']:.3f} m

Área de aço calculada:
As_calc = {data['As_calc']:.2f} cm²

Área mínima:
As_min = {data['As_min']:.2f} cm²

Área adotada:
As_adotada = {data['As_required']:.2f} cm²

Taxa de armadura:
ρ = {data['rho']:.4f}

Taxa máxima:
ρ_max = {data['rho_max']:.4f}

Armadura longitudinal:
{data['n_bars']} barras Ø{data['diameter']} mm

Área fornecida:
As_fornecida = {data['As_provided']:.2f} cm²

-------------- CISALHAMENTO ------------

Cortante solicitante:
Vd = {data['Vd']:.2f} kN

Parcela resistente do concreto:
Vc = {data['Vc']:.2f} kN

Parcela resistente do aço:
Vs = {data['Vs']:.2f} kN

Limite resistente:
Vrd2 = {data['Vrd2']:.2f} kN

Detalhamento transversal:
{stirrup_type}

Estribo:
Ø{data['phi_stirrup']} mm

Espaçamento:
{data['spacing']:.1f} cm

------------------------------------------------

Sistema IStruct
Ferramenta de apoio ao dimensionamento estrutural

Base:
NBR 6118 (modelo simplificado)

O engenheiro responsável deve validar os resultados.
"""

    return report