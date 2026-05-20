from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    HRFlowable,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import A4

from reportlab.lib.enums import TA_CENTER

from reportlab.lib import colors

from datetime import datetime

import os

from utils.paths import get_asset_path

def export_pdf(
    filename,
    report_text,
    section_image=None
):

    doc = SimpleDocTemplate(

        filename,

        pagesize=A4,

        rightMargin=40,
        leftMargin=40,

        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==================================================
    # ESTILOS
    # ==================================================

    center_style = ParagraphStyle(

        "Center",

        parent=styles["Normal"],

        alignment=TA_CENTER,

        fontSize=11,

        leading=16
    )

    body_style = ParagraphStyle(

        "Body",

        parent=styles["BodyText"],

        fontSize=10,

        leading=15
    )

    # ==================================================
    # CABEÇALHO
    # ==================================================

    logo_path = get_asset_path("logo.png")

    logo = None

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=60,
            height=60
        )

    title = Paragraph(

        (
            "<b>MEMORIAL DE CÁLCULO</b><br/>"
            "Dimensionamento de Viga "
            "em Concreto Armado"
        ),

        center_style
    )

    header_data = [
        [logo, title]
    ]

    header = Table(
        header_data,
        colWidths=[80, 400]
    )

    header.setStyle(

        TableStyle([

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("ALIGN", (0, 0), (0, 0), "LEFT"),

            ("ALIGN", (1, 0), (1, 0), "CENTER")
        ])
    )

    elements.append(header)

    elements.append(
        Spacer(1, 15)
    )

    elements.append(
        HRFlowable(
            width="100%",
            color=colors.black
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # ==================================================
    # INFORMAÇÕES
    # ==================================================

    current_date = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    info_text = f"""

    <b>Software:</b> IStruct Beam / ISTruct Vigas<br/>

    <b>Empresa:</b> ISENG Structural<br/>

    <b>Data:</b> {current_date}

    """

    info = Paragraph(
        info_text,
        body_style
    )

    elements.append(info)

    elements.append(
        Spacer(1, 15)
    )

    # ==================================================
    # IMAGEM DA SEÇÃO
    # ==================================================

    if section_image and os.path.exists(section_image):

        section_title = Paragraph(

            "<b>SEÇÃO TRANSVERSAL</b>",

            styles["Heading2"]
        )

        elements.append(section_title)

        elements.append(
            Spacer(1, 10)
        )

        img = Image(
            section_image,
            width=250,
            height=180
        )

        img.hAlign = "CENTER"

        elements.append(img)

        elements.append(
            Spacer(1, 20)
        )

    # ==================================================
    # RESULTADOS
    # ==================================================

    section_title = Paragraph(

        "<b>RESULTADOS</b>",

        styles["Heading2"]
    )

    elements.append(section_title)

    elements.append(
        Spacer(1, 10)
    )

    lines = report_text.split("\n")

    for line in lines:

        if not line.strip():
            continue

        p = Paragraph(

            line.replace(
                " ",
                "&nbsp;"
            ),

            body_style
        )

        elements.append(p)

        elements.append(
            Spacer(1, 5)
        )

    # ==================================================
    # RODAPÉ
    # ==================================================

    elements.append(
        Spacer(1, 30)
    )

    elements.append(
        HRFlowable(
            width="100%",
            color=colors.grey
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    footer = Paragraph(

        (
            "Documento gerado automaticamente "
            "pelo IStruct Beam"
        ),

        center_style
    )

    elements.append(footer)

    # ==================================================
    # BUILD
    # ==================================================

    doc.build(elements)