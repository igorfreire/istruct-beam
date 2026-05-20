class RectangularSection:
    def __init__(self, bw: float, h: float, cover: float, bar_diameter: float):
        self.bw = bw  # cm
        self.h = h    # cm
        self.cover = cover
        self.bar_diameter = bar_diameter

    @property
    def d(self):
        return self.h - self.cover - self.bar_diameter / 2