from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualMapWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualMapWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.map_text_edit]
        apply_tab_texts(self.objectName(), self.manual_map_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_map_tab_widget = QTabWidget()
        self.map_text_edit = QTextEdit()
        self.map_text_edit.setObjectName("mapTextEdit")
        self.map_text_edit.setReadOnly(True)
        self.map_text_edit.setText("map")
        self.manual_map_tab_widget.addTab(self.map_text_edit, "")
        main_layout.addWidget(self.manual_map_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_map_tab_widget.setCurrentIndex(index)