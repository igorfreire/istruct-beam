from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton
)

from PyQt5.QtGui import QFont


class ReportDialog(QDialog):

    def __init__(self, report_text):

        super().__init__()

        self.setWindowTitle(
            "Memória de Cálculo"
        )

        self.resize(700, 600)

        layout = QVBoxLayout()

        # ==========================================
        # TEXTO DO RELATÓRIO
        # ==========================================

        self.report_area = QTextEdit()

        self.report_area.setReadOnly(True)

        self.report_area.setFont(
            QFont("Consolas", 10)
        )

        self.report_area.setText(
            report_text
        )

        layout.addWidget(
            self.report_area
        )

        # ==========================================
        # BOTÃO FECHAR
        # ==========================================

        self.close_button = QPushButton(
            "Fechar"
        )

        self.close_button.clicked.connect(
            self.close
        )

        layout.addWidget(
            self.close_button
        )

        self.setLayout(layout)