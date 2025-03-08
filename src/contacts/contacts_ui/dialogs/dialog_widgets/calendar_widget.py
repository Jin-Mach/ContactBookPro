from typing import Optional

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QCalendarWidget


class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("calendarWidget")
        self.setGridVisible(True)
        self.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)

    def set_today(self) -> None:
        self.showToday()
        self.setSelectedDate(QDate.currentDate())

    def return_selected_date(self) -> Optional[str]:
        current_date = QDate.currentDate()
        selected_date = self.selectedDate()
        if selected_date < current_date:
            return selected_date.toString("dd.MM.yyyy")
        return None