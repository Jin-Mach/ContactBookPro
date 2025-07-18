from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class RelationshipBarChartWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("relationshipBarChartWidget")
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
                color_map = {
                    "1": "#ff6f61",
                    "2": "#fbc02d",
                    "3": "#4db6ac",
                    "4": "#64b5f6",
                    "5": "#ba68c8",
                    "6": "#81c784",
                }
                sizes = []
                labels = []
                colors = []
                for index, label, size in data:
                    colors.append(color_map.get(str(index), ""))
                    labels.append(label)
                    sizes.append(size)
                place.bar(labels, sizes, color=colors)
            self.figure.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)