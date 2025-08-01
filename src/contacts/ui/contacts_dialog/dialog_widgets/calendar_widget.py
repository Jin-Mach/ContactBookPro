from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QCalendarWidget, QToolButton

from src.utilities.icon_provider import IconProvider


class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("calendarWidget")
        self.setGridVisible(True)
        self.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.NoHorizontalHeader)
        self.setStyleSheet("""
            QCalendarWidget QSpinBox {
                width: 60px;
            }
        """)
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QToolButton), None, self)

    def set_today(self) -> None:
        self.showToday()
        self.setSelectedDate(QDate.currentDate())

    def return_selected_date(self) -> str | None:
        current_date = QDate.currentDate()
        selected_date = self.selectedDate()
        if selected_date < current_date:
            return selected_date.toString("yyyy-MM-dd")
        return None