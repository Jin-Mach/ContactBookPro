from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class CompletionBarChartWidget(QWidget):
    def __init__(self, total: bool, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("completionBarChartWidget")
        self.total = total
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
            place.yaxis.set_major_locator(MaxNLocator(integer=True))
            place.set_facecolor("#31363b")
            place.tick_params(axis="x", colors="#ffffff")
            place.tick_params(axis="y", colors="#ffffff")
            place.spines["left"].set_color("#ffffff")
            place.spines["top"].set_visible(False)
            place.spines["right"].set_visible(False)
            place.spines["bottom"].set_color("#ffffff")
            is_data = False
            for value in data.values():
                if value != (0, 0):
                    is_data = True
                    break
            if not is_data:
                place.text(0.5, 0.5, ui_text.get("noData", ""), fontsize=14, ha='center', va='center',
                           transform=place.transAxes, color="#ffffff")
                for spine in place.spines.values():
                    spine.set_visible(False)
                place.set_xticks([])
                place.set_yticks([])
                place.tick_params(left=False, bottom=False)
                return
            if self.total:
                place.yaxis.set_major_locator(MaxNLocator(nbins=1))
                place.set_yticks([0])
                place.set_ylim(-0.5, 0.5)
                place.get_xaxis().set_visible(False)
                place.tick_params(axis='y', which='both', length=0)
                place.spines["left"].set_visible(False)
                place.spines["top"].set_visible(False)
                place.spines["bottom"].set_visible(False)
                place.spines["right"].set_visible(False)
                total = 0
                filled = 0
                for table_data in data.values():
                    total += table_data[0]
                    filled += table_data[1]
                labels = [ui_text.get("total", "")]
                if total != 0:
                    values = [(filled / total) * 100]
                else:
                    values = [0]
                bars = place.barh(labels, values, color="red")
                for bar in bars:
                    width = bar.get_width()
                    y = bar.get_y() + bar.get_height() / 2
                    place.text(width + 1, y, f"{width:.1f}%", va='center', color="#ffffff", fontsize=10)
            else:
                place.set_title(ui_text.get("title", ""), pad=15, color="#ffffff", fontsize=12)
                labels = []
                values = []
                for key in data.keys():
                    labels.append(ui_text.get(key, ""))
                for counts in data.values():
                    total = counts[0]
                    filled = counts[1]
                    if total != 0:
                        values.append((filled / total) * 100)
                    else:
                        values.append(0)
                bars = place.barh(labels, values, color="#64b5f6")
                for bar in bars:
                    width = bar.get_width()
                    y = bar.get_y() + bar.get_height() / 2
                    place.text(width + 1, y, f"{width:.1f}%", va='center', color="#ffffff", fontsize=10)
            self.figure.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)