from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class SocialBarCharWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("socialBarChartWidget")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        return main_layout

    def draw_bar(self, data: dict):
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            self.figure.clear()
            width = 0.35
            self.figure.set_facecolor("#31363b")
            place = self.figure.add_subplot(111)
            place.set_facecolor("#31363b")
            place.spines["left"].set_visible(False)
            place.spines["top"].set_visible(False)
            place.spines["right"].set_visible(False)
            place.spines["bottom"].set_color("#ffffff")
            is_data = False
            for value in data.values():
                if value != ("", ""):
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
            place.set_title(ui_text.get("title", ""), pad=20, color="#ffffff", fontsize=12)
            place.tick_params(axis="x", colors="#ffffff")
            place.tick_params(axis="y", colors="#ffffff")
            place.yaxis.set_major_locator(MaxNLocator(integer=True))
            categories_names = list(data.keys())
            categories_names[1] = ui_text.get(categories_names[1], "")
            categories_names[-1] = ui_text.get(categories_names[-1], "")
            filled_values = []
            empty_values = []
            for value_tuple in data.values():
                filled_values.append(value_tuple[0])
                empty_values.append(value_tuple[1])
            categories_positions = []
            for index in range(len(categories_names)):
                categories_positions.append(index)
            filled_positions = []
            for pos in categories_positions:
                filled_positions.append(pos - width / 2)
            empty_positions = []
            for pos in categories_positions:
                empty_positions.append(pos + width / 2)
            place.bar(filled_positions, filled_values, width=width, label=ui_text.get("filled", ""), color="#4caf50")
            place.bar(empty_positions, empty_values, width=width, label=ui_text.get("empty", ""), color="#f44336")
            place.set_xticks(categories_positions)
            place.set_xticklabels(categories_names)
            place.legend(loc="upper left", bbox_to_anchor=(0.75, 1.15))
            for i in range(len(filled_values)):
                try:
                    y = float(filled_values[i]) + 0.1
                except (ValueError, TypeError):
                    y = 0.1
                place.text(filled_positions[i], y, str(filled_values[i]), ha='center', va='bottom', color="#ffffff")
            for i in range(len(empty_values)):
                try:
                    y = float(empty_values[i]) + 0.1
                except (ValueError, TypeError):
                    y = 0.1
                place.text(empty_positions[i], y, str(empty_values[i]), ha='center', va='bottom', color="#ffffff")
            place.set_yticks([])
            place.tick_params(left=False)
            self.canvas.draw()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
