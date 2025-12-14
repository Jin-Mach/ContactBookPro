from typing import TYPE_CHECKING

from PyQt6.QtCore import QTime, QTimer, QDate
from PyQt6.QtWidgets import QStatusBar, QLabel, QPushButton, QWidget

from src.application.main_window_widgets.holidays_dialog import HolidaysDialog
from src.utilities.language_provider import LanguageProvider
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.application.main_window import MainWindow


# noinspection PyUnresolvedReferences
class StatusBar(QStatusBar):
    def __init__(self, parent: "MainWindow") -> None:
        super().__init__(parent)
        self.setObjectName("statusBar")
        self.parent = parent
        self.create_gui()
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.align_time_to_minute()

    def create_gui(self) -> None:
        spacer = QWidget()
        spacer.setFixedWidth(10)
        self.holidays_label = QLabel()
        self.holidays_button = QPushButton()
        self.holidays_button.setObjectName("holidaysButton")
        self.holidays_button.setFixedHeight(20)
        self.holidays_button.clicked.connect(self.show_holidays_dialog)
        self.time_label = QLabel()
        self.addPermanentWidget(self.holidays_label)
        self.addPermanentWidget(self.holidays_button)
        self.addPermanentWidget(spacer)
        self.addPermanentWidget(self.time_label)
        self.addPermanentWidget(spacer)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_json_text("tooltips_text.json", self.objectName())
            if tooltips_text:
                self.holidays_button.setToolTip(tooltips_text.get(self.holidays_button.objectName(), ""))
                self.holidays_button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e)

    def show_status_bar_message(self, message: str) -> None:
        self.showMessage(message, 5000)

    def update_time(self) -> None:
        current_date = QDate.currentDate().toString("dd.MM.yyyy")
        current_time = QTime.currentTime().toString("HH:mm")
        self.holidays_label.setText(current_date)
        self.holidays_button.setText(current_date)
        self.time_label.setText(current_time)

    def align_time_to_minute(self) -> None:
        now = QTime.currentTime()
        to_next_minute = (60 - now.second()) * 1000 - now.second()
        QTimer.singleShot(to_next_minute, self.start_minute_timer)

    def start_minute_timer(self) -> None:
        self.update_time()
        self.timer.start(60 * 1000)

    def show_holidays_dialog(self) -> None:
        dialog = HolidaysDialog(self.parent.holiday_data, self)
        dialog.show()