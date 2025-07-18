from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class CityBarChartWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("cityBarCharWidget")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        return main_layout

    def draw_bar(self, data: dict) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
            self.figure.clear()
            self.figure.set_facecolor("#31363b")
            place = self.figure.add_subplot(111)
            place.set_title(ui_text.get("title", ""), color="#ffffff", fontsize=12)
            place.yaxis.set_major_locator(MaxNLocator(integer=True))
            place.set_facecolor("#31363b")
            place.tick_params(axis="x", colors="#ffffff")
            place.tick_params(axis="y", colors="#ffffff")
            place.spines["top"].set_visible(False)
            place.spines["right"].set_visible(False)
            place.spines["bottom"].set_color("#ffffff")
            place.spines["left"].set_color("#ffffff")
            if not data:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                place.set_xticks([])
                place.set_yticks([])
            else:
                sizes = []
                labels = []
                colors = ["#ff6f61", "#fbc02d", "#4db6ac", "#64b5f6", "#ba68c8", "#81c784"]
                main = 5
                top_items = sorted_data[:main]
                others_items = sorted_data[main:]
                for label, size in top_items:
                    labels.append(label)
                    sizes.append(size)
                others_size = 0
                for _, size in others_items:
                    others_size += size
                if others_size > 0:
                    labels.append(ui_text.get("others", ""))
                    sizes.append(others_size)
                place.bar(labels, sizes, color=colors)
            self.figure.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)