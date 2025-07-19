from typing import Callable

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class GenderPieChartWidget(QWidget):
    def __init__(self, total_count: Callable[[], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("genderPieChartWidget")
        self.total_count = total_count
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        return main_layout

    def draw_pie(self, data: dict) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            self.figure.clear()
            self.figure.set_facecolor("#31363b")
            place = self.figure.add_subplot(111)
            place.set_title(ui_text.get("title", ""), color="#ffffff", fontsize=12)
            place.set_facecolor("#31363b")
            if not data:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                place.set_xticks([])
                place.set_yticks([])
            else:
                color_map = {
                    "1": "#448aff",
                    "2": "#ff99bb"
                }
                sizes = []
                labels = []
                colors = []
                for index, label, size in data:
                    colors.append(color_map.get(str(index)))
                    labels.append(label)
                    sizes.append(size)
                _, label_text , _ = place.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90,
                                              counterclock=False)
                for label in label_text:
                    label.set_color("#ffffff")
                place.axis("equal")
            self.figure.canvas.draw()
            self.total_count()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)