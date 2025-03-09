import pathlib
from typing import Optional

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QCalendarWidget, QToolButton

from src.utilities.error_handler import ErrorHandler


class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("calendarWidget")
        self.setGridVisible(True)
        self.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.NoHorizontalHeader)
        self.set_icons()

    def set_icons(self) -> None:
        icons_path = pathlib.Path(__file__).parent.parent.parent.parent.parent.joinpath("icons", "calendar_icons")
        try:
            self.findChild(QToolButton, "qt_calendar_prevmonth").setIcon(QIcon(str(icons_path.joinpath("left_arrow.png"))))
            self.findChild(QToolButton, "qt_calendar_nextmonth").setIcon(QIcon(str(icons_path.joinpath("right_arrow.png"))))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_today(self) -> None:
        self.showToday()
        self.setSelectedDate(QDate.currentDate())

    def return_selected_date(self) -> Optional[str]:
        current_date = QDate.currentDate()
        selected_date = self.selectedDate()
        if selected_date < current_date:
            return selected_date.toString("dd.MM.yyyy")
        return None