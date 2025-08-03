from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QHBoxLayout, QStackedWidget

from src.manual.ui.manual_widgets.manual_treewidget import ManualTreeWidget
from src.utilities.error_handler import ErrorHandler


class ManualMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualMainWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        self.tree_widget = ManualTreeWidget(self)
        self.tree_widget.itemClicked.connect(self.set_stacked_widget)
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.tree_widget, stretch=0)
        main_layout.addWidget(self.stacked_widget, stretch=1)
        return main_layout

    def set_stacked_widget(self) -> None:
        try:
            stacked_index, tab_index = self.tree_widget.currentItem().data(0, Qt.ItemDataRole.UserRole)
            print("stacked index:", stacked_index)
            print("tab_index:", tab_index)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)