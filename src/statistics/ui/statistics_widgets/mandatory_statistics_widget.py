from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QMainWindow, QLabel

from src.statistics.ui.statistics_widgets.chart_widgets.relationship_bar_chart_widget import RelationshipBarChartWidget
from src.statistics.ui.statistics_widgets.chart_widgets.gender_pie_chart_widget import GenderPieChartWidget
from src.statistics.ui.statistics_widgets.chart_widgets.city_bar_chart_widget import CityBarChartWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel


class MandatoryStatisticsWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", main_window: QMainWindow,
                 parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mandatoryStatisticsWidget")
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.main_window = main_window
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        self.count_label = QLabel()
        self.count_label.setStyleSheet("font-size: 25px")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gender_pie = GenderPieChartWidget(self.set_contacts_count, self)
        self.relationship_bar = RelationshipBarChartWidget(self)
        self.city_bar = CityBarChartWidget(self)
        main_layout.addWidget(self.count_label, 0, 0, 1, 2)
        main_layout.addWidget(self.gender_pie, 1, 0)
        main_layout.addWidget(self.relationship_bar, 1, 1)
        main_layout.addWidget(self.city_bar, 2, 0, 1, 2)
        return main_layout

    def set_contacts_count(self) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            self.count_label.setText(f"{ui_text.get("totalCount", "")} {self.mandatory_model.rowCount()}")
        except Exception as e:
            ErrorHandler.exception_handler(e, self)