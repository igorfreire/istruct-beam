import os

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QMessageBox,
    QFileDialog
)

from PyQt5.QtGui import QFont

from core.materials import Concrete, Steel
from core.sections import RectangularSection

from design.beam.analysis import SimpleBeamAnalysis
from design.beam.flexure import BeamFlexure
from design.beam.shear import BeamShear

from detailing.rebar import choose_bars

from reports.beam_report import generate_beam_report
from reports.pdf_report import export_pdf

from gui.drawing_widget import BeamDrawingWidget

from gui.dialogs.report_dialog import (
    ReportDialog
)


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.report_text = ""

        self.setWindowTitle(
            "IStruct - Dimensionamento de Vigas"
        )

        self.resize(900, 700)

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        # ==============================================
        # TÍTULO
        # ==============================================

        title = QLabel(
            "IStruct — Dimensionamento de Vigas"
        )

        title.setFont(
            QFont("Arial", 14, QFont.Bold)
        )

        main_layout.addWidget(title)

        # ==============================================
        # FORMULÁRIO
        # ==============================================

        form_layout = QFormLayout()

        def create_input():

            field = QLineEdit()

            field.setFixedWidth(120)

            return field

        self.span_input = create_input()
        self.load_input = create_input()

        self.fck_input = create_input()

        self.bw_input = create_input()
        self.h_input = create_input()

        self.cover_input = create_input()

        self.phi_input = create_input()

        form_layout.addRow(
            "Vão (m):",
            self.span_input
        )

        form_layout.addRow(
            "Carga distribuída (kN/m):",
            self.load_input
        )

        form_layout.addRow(
            "fck (MPa):",
            self.fck_input
        )

        form_layout.addRow(
            "bw (cm):",
            self.bw_input
        )

        form_layout.addRow(
            "h (cm):",
            self.h_input
        )

        form_layout.addRow(
            "Cobrimento (cm):",
            self.cover_input
        )

        form_layout.addRow(
            "φ barra longitudinal (mm):",
            self.phi_input
        )

        main_layout.addLayout(
            form_layout
        )

        # ==============================================
        # BOTÕES
        # ==============================================

        buttons_layout = QHBoxLayout()

        # CALCULAR

        self.calculate_button = QPushButton(
            "Calcular"
        )

        self.calculate_button.clicked.connect(
            self.calculate_beam
        )

        buttons_layout.addWidget(
            self.calculate_button
        )

        # MEMORIAL

        self.report_button = QPushButton(
            "Memória de Cálculo"
        )

        self.report_button.clicked.connect(
            self.show_report
        )

        buttons_layout.addWidget(
            self.report_button
        )

        # EXPORTAR PDF

        self.pdf_button = QPushButton(
            "Exportar PDF"
        )

        self.pdf_button.clicked.connect(
            self.export_pdf_report
        )

        buttons_layout.addWidget(
            self.pdf_button
        )

        # LIMPAR

        self.clear_button = QPushButton(
            "Limpar"
        )

        self.clear_button.clicked.connect(
            self.clear_fields
        )

        buttons_layout.addWidget(
            self.clear_button
        )

        # SAIR

        self.exit_button = QPushButton(
            "Sair"
        )

        self.exit_button.clicked.connect(
            self.close
        )

        buttons_layout.addWidget(
            self.exit_button
        )

        main_layout.addLayout(
            buttons_layout
        )

        # ==============================================
        # RESUMO
        # ==============================================

        self.summary_label = QLabel(
            "Nenhum cálculo realizado."
        )

        self.summary_label.setFont(
            QFont("Arial", 10)
        )

        main_layout.addWidget(
            self.summary_label
        )

        # ==============================================
        # DESENHO
        # ==============================================

        self.drawing = BeamDrawingWidget()

        main_layout.addWidget(
            self.drawing
        )

        self.setLayout(main_layout)

    # ==================================================
    # LIMPAR
    # ==================================================

    def clear_fields(self):

        self.span_input.clear()

        self.load_input.clear()

        self.fck_input.clear()

        self.bw_input.clear()

        self.h_input.clear()

        self.cover_input.clear()

        self.phi_input.clear()

        self.summary_label.setText(
            "Nenhum cálculo realizado."
        )

    # ==================================================
    # MEMÓRIA DE CÁLCULO
    # ==================================================

    def show_report(self):

        if not self.report_text:

            QMessageBox.warning(
                self,
                "Aviso",
                "Execute um cálculo primeiro."
            )

            return

        dialog = ReportDialog(
            self.report_text
        )

        dialog.exec_()

    # ==================================================
    # EXPORTAR PDF
    # ==================================================

    def export_pdf_report(self):

        if not self.report_text:

            QMessageBox.warning(
                self,
                "Aviso",
                "Execute um cálculo primeiro."
            )

            return

        filename, _ = QFileDialog.getSaveFileName(

            self,

            "Salvar PDF",

            "memorial_viga.pdf",

            "PDF Files (*.pdf)"
        )

        if not filename:
            return

        try:

            # ==========================================
            # EXPORTA IMAGEM TEMPORÁRIA
            # ==========================================

            temp_image = "temp_section.png"

            self.drawing.export_image(
                temp_image
            )

            # ==========================================
            # EXPORTA PDF
            # ==========================================

            export_pdf(
                filename,
                self.report_text,
                temp_image
            )

            # ==========================================
            # REMOVE IMAGEM TEMP
            # ==========================================

            if os.path.exists(temp_image):

                os.remove(temp_image)

            QMessageBox.information(
                self,
                "Sucesso",
                "PDF exportado com sucesso."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # ==================================================
    # CÁLCULO
    # ==================================================

    def calculate_beam(self):

        try:

            # ==========================================
            # INPUTS
            # ==========================================

            L = float(
                self.span_input.text()
            )

            q = float(
                self.load_input.text()
            )

            fck = float(
                self.fck_input.text()
            )

            bw = float(
                self.bw_input.text()
            )

            h = float(
                self.h_input.text()
            )

            cover = float(
                self.cover_input.text()
            )

            phi = float(
                self.phi_input.text()
            )

            # ==========================================
            # ANÁLISE
            # ==========================================

            analysis = SimpleBeamAnalysis(
                L,
                q
            )

            efforts = analysis.calculate()

            Md = efforts["Mmax_kNm"]

            Vd = efforts["Vmax_kN"]

            # ==========================================
            # MATERIAIS
            # ==========================================

            concrete = Concrete(fck)

            steel = Steel()

            # ==========================================
            # SEÇÃO
            # ==========================================

            section = RectangularSection(
                bw,
                h,
                cover,
                phi
            )

            # ==========================================
            # FLEXÃO
            # ==========================================

            flex = BeamFlexure(
                section,
                concrete,
                steel,
                Md
            )

            flex_result = flex.calculate()

            if flex_result.get("error"):

                QMessageBox.critical(
                    self,
                    "Erro de Flexão",
                    flex_result["message"]
                )

                return

            # ==========================================
            # ARMADURA
            # ==========================================

            rebar = choose_bars(
                flex_result["As_cm2"]
            )

            # ==========================================
            # CISALHAMENTO
            # ==========================================

            shear = BeamShear(
                section,
                concrete,
                steel,
                Vd
            )

            shear_result = shear.calculate()

            if shear_result.get("error"):

                QMessageBox.critical(
                    self,
                    "Erro de Cisalhamento",
                    shear_result["message"]
                )

                return

            # ==========================================
            # DESENHO
            # ==========================================

            drawing_data = {

                "bw": bw,

                "h": h,

                "cover": cover,

                "n_bars":
                    rebar["n_bars"],

                "bar_diameter":
                    rebar["diameter_mm"]
            }

            self.drawing.update_section(
                drawing_data
            )

            # ==========================================
            # RESUMO
            # ==========================================

            self.summary_label.setText(

                (
                    f"Md = {Md:.2f} kN.m   |   "

                    f"{rebar['n_bars']}Ø"
                    f"{rebar['diameter_mm']} mm   |   "

                    f"Ø{shear_result['phi_mm']} "
                    f"c/{shear_result['spacing_cm']:.1f} cm"
                )
            )

            # ==========================================
            # RELATÓRIO
            # ==========================================

            report_data = {

                "Md": Md,

                "d":
                    flex_result["d_m"],

                "x":
                    flex_result["x_m"],

                "x_lim":
                    flex_result["x_lim_m"],

                "z":
                    flex_result["z_m"],

                "rho":
                    flex_result["rho"],

                "rho_max":
                    flex_result["rho_max"],

                "As_calc":
                    flex_result[
                        "As_calc_cm2"
                    ],

                "As_min":
                    flex_result[
                        "As_min_cm2"
                    ],

                "As_required":
                    flex_result[
                        "As_cm2"
                    ],

                "n_bars":
                    rebar["n_bars"],

                "diameter":
                    rebar["diameter_mm"],

                "As_provided":
                    rebar["As_provided"],

                "Vd": Vd,

                "Vc":
                    shear_result["Vc_kN"],

                "Vs":
                    shear_result["Vs_kN"],

                "Vrd2":
                    shear_result["Vrd2_kN"],

                "spacing":
                    shear_result[
                        "spacing_cm"
                    ],

                "phi_stirrup":
                    shear_result["phi_mm"],

                "minimum_stirrup":
                    shear_result[
                        "is_minimum_stirrup"
                    ]
            }

            self.report_text = (
                generate_beam_report(
                    report_data
                )
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )