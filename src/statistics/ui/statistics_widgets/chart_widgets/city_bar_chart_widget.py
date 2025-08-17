from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class CityBarChartWidget(QWidget):
    def __init__(self, column_name=None, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("cityBarCharWidget")
        self.column_name = column_name
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
            if self.column_name != "work":
                data = [data, [0]]
            sorted_data = sorted(data[0], key=lambda x: x[1], reverse=True)
            self.figure.clear()
            self.figure.set_facecolor("#31363b")
            place = self.figure.add_subplot(111)
            place.set_facecolor("#31363b")
            place.yaxis.set_major_locator(MaxNLocator(integer=True))
            place.tick_params(axis="x", colors="#ffffff")
            place.tick_params(axis="y", colors="#ffffff")
            place.spines["left"].set_visible(False)
            place.spines["top"].set_visible(False)
            place.spines["right"].set_visible(False)
            place.spines["bottom"].set_color("#ffffff")
            try:
                value = int(data[1][0])
            except (ValueError, TypeError):
                value = 0
            if self.column_name == "work" and not sorted_data and value > 0:
                place.set_title(ui_text.get("title", ""), pad=15, color="#ffffff", fontsize=12)
                labels = [ui_text.get("unfilled", "")]
                sizes = [data[1][0]]
                colors = ["#4db6ac"]
                titles = place.bar(labels, sizes, color=colors)
                place.bar_label(titles, padding=3, color="#ffffff", fontsize=10)
                place.set_yticks([])
                place.tick_params(left=False)
                self.figure.canvas.draw()
                return
            if not sorted_data:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                place.spines["bottom"].set_visible(False)
                place.set_xticks([])
                place.set_yticks([])
                place.tick_params(left=False)
                return
            sizes = []
            labels = []
            colors = ["#ff6f61", "#fbc02d", "#4db6ac", "#64b5f6", "#81c784"]
            main = 5
            if self.column_name == "work":
                main = 4
            top_items = sorted_data[:main]
            others_items = sorted_data[main:]
            for label, size in top_items:
                labels.append(label)
                sizes.append(size)
            others_size = sum(size for _, size in others_items)
            if others_size > 0:
                labels.append(ui_text.get("others", ""))
                sizes.append(others_size)
            if self.column_name == "work":
                labels.append(ui_text.get("unfilled", ""))
                sizes.append(data[1][0])
            place.set_title(ui_text.get("title", ""), pad=15, color="#ffffff", fontsize=12)
            titles = place.bar(labels, sizes, color=colors)
            place.bar_label(titles, padding=3, color="#ffffff", fontsize=10)
            place.set_yticks([])
            place.tick_params(left=False)
            self.figure.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)