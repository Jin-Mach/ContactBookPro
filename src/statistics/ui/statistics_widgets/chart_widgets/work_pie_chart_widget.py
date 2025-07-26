from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class WorkPieChartWidget(QWidget):
    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("workPieChartWidget")
        self.title = title
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
            place.set_facecolor("#31363b")
            if not data:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                place.spines["left"].set_visible(False)
                place.spines["top"].set_visible(False)
                place.spines["right"].set_visible(False)
                place.spines["bottom"].set_visible(False)
                place.set_xticks([])
                place.set_yticks([])
                place.tick_params(left=False)
                return
            sizes = []
            labels = []
            colors = ["#448aff", "#bbdefb"]
            for label, size in data:
                labels.append(ui_text.get(label, ""))
                try:
                    sizes.append(float(size))
                except (ValueError, TypeError):
                    sizes.append(0)
            if sum(sizes) == 0:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                place.spines["left"].set_visible(False)
                place.spines["top"].set_visible(False)
                place.spines["right"].set_visible(False)
                place.spines["bottom"].set_visible(False)
                place.set_xticks([])
                place.set_yticks([])
                place.tick_params(left=False)
            else:
                place.set_title(ui_text.get(self.title, ""), pad=15, color="#ffffff", fontsize=12)
                _, label_text, _ = place.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90,
                                             counterclock=False)
                for label in label_text:
                    label.set_color("#ffffff")
                place.axis("equal")
            self.figure.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)