from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualStatisticsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualStatisticsWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.statistics_text_edit]
        apply_tab_texts(self.objectName(), self.manual_statistics_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_statistics_tab_widget = QTabWidget()
        self.statistics_text_edit = QTextEdit()
        self.statistics_text_edit.setObjectName("statisticsTextEdit")
        self.statistics_text_edit.setReadOnly(True)
        self.statistics_text_edit.setText("statistics")
        self.manual_statistics_tab_widget.addTab(self.statistics_text_edit, "")
        main_layout.addWidget(self.manual_statistics_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_statistics_tab_widget.setCurrentIndex(index)