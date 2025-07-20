from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout
from matplotlib.ticker import MaxNLocator

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class CompletionBarChartWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("completionBartChartWidget")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        return main_layout

    def draw_bar(self, data: dict[str, tuple[int, int]]) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            self.figure.clear()
            self.figure.set_facecolor("#31363b")
            place = self.figure.add_subplot(111)
            place.set_title(ui_text.get("title", ""), pad=15, color="#ffffff", fontsize=12)
            place.yaxis.set_major_locator(MaxNLocator(integer=True))
            place.set_facecolor("#31363b")
            place.tick_params(axis="x", colors="#ffffff")
            place.tick_params(axis="y", colors="#ffffff")
            place.spines["left"].set_color("#ffffff")
            place.spines["top"].set_visible(False)
            place.spines["right"].set_visible(False)
            place.spines["bottom"].set_color("#ffffff")
            if not data:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                place.set_xticks([])
                place.set_yticks([])
                place.tick_params(left=False)
                return
            labels = []
            values = []
            for key in data.keys():
                labels.append(ui_text.get(key, ""))
            for counts in data.values():
                values.append((counts[1] / counts[0]) * 100)
            bars = place.barh(labels, values, color="#64b5f6")
            for bar in bars:
                width = bar.get_width()
                y = bar.get_y() + bar.get_height() / 2
                place.text(width + 1, y, f"{width:.1f}%", va='center', color="#ffffff", fontsize=10)
            self.figure.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)