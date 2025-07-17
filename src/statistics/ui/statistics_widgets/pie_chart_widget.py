from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout


class PieChartWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("pieChartWidget")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        return main_layout

    def draw_pie(self, data: dict) -> None:
        color_map = {
            "1": "#448aff",
            "2": "#ffccdb"
        }
        sizes = []
        labels = []
        colors = []
        for index, label, size in data:
            colors.append(color_map.get(str(index)))
            labels.append(label)
            sizes.append(size)
        self.figure.clear()
        self.figure.set_facecolor("#31363b")
        place = self.figure.add_subplot(111)
        _, label_text , _ = place.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
        for label in label_text:
            label.set_color("#ffffff")
        place.axis("equal")
        self.figure.canvas.draw()