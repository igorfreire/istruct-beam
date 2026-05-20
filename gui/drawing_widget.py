from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import (
    QPainter,
    QPen,
    QColor,
    QBrush,
    QPixmap
)

from PyQt5.QtCore import Qt


class BeamDrawingWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.section_data = None

        self.setMinimumHeight(300)

    # ==================================================
    # UPDATE
    # ==================================================

    def update_section(
        self,
        section_data
    ):

        self.section_data = section_data

        self.update()

    # ==================================================
    # EXPORT IMAGE
    # ==================================================

    def export_image(
        self,
        filename
    ):

        pixmap = QPixmap(
            self.size()
        )

        self.render(pixmap)

        pixmap.save(filename)

    # ==================================================
    # PAINT
    # ==================================================

    def paintEvent(self, event):

        if not self.section_data:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # ==============================================
        # DADOS
        # ==============================================

        bw = self.section_data["bw"]

        h = self.section_data["h"]

        cover = self.section_data["cover"]

        n_bars = self.section_data["n_bars"]

        bar_diameter = self.section_data[
            "bar_diameter"
        ]

        # ==============================================
        # ESCALA
        # ==============================================

        scale = 5

        beam_w = int(bw * scale)

        beam_h = int(h * scale)

        start_x = int(
            (self.width() - beam_w) / 2
        )

        start_y = 40

        # ==============================================
        # CONCRETO
        # ==============================================

        painter.setBrush(
            QBrush(
                QColor(230, 230, 230)
            )
        )

        painter.setPen(
            QPen(Qt.black, 2)
        )

        painter.drawRect(
            start_x,
            start_y,
            beam_w,
            beam_h
        )

        # ==============================================
        # ESTRIBO
        # ==============================================

        cover_px = int(cover * scale)

        stirrup_x = start_x + cover_px

        stirrup_y = start_y + cover_px

        stirrup_w = beam_w - 2 * cover_px

        stirrup_h = beam_h - 2 * cover_px

        painter.setPen(
            QPen(
                QColor(0, 90, 180),
                2
            )
        )

        painter.drawRect(
            stirrup_x,
            stirrup_y,
            stirrup_w,
            stirrup_h
        )

        # ==============================================
        # BARRAS
        # ==============================================

        painter.setBrush(
            QBrush(
                QColor(200, 30, 30)
            )
        )

        if n_bars == 1:

            x_positions = [
                start_x + beam_w / 2
            ]

        else:

            spacing = (
                stirrup_w /
                (n_bars - 1)
            )

            x_positions = [

                stirrup_x + i * spacing

                for i in range(n_bars)
            ]

        y_bar = (
            start_y +
            beam_h -
            cover_px -
            10
        )

        for x in x_positions:

            painter.drawEllipse(
                int(x - 6),
                int(y_bar - 6),
                12,
                12
            )

        # ==============================================
        # TEXTOS
        # ==============================================

        painter.setPen(
            QPen(Qt.black)
        )

        painter.drawText(
            start_x,
            start_y - 10,
            f"{bw} x {h} cm"
        )

        painter.drawText(
            start_x,
            start_y + beam_h + 25,
            (
                f"{n_bars}Ø"
                f"{bar_diameter} mm"
            )
        )

        painter.end()   