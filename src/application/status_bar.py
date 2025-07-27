from PyQt6.QtCore import QTime, QTimer
from PyQt6.QtWidgets import QStatusBar, QLabel


# noinspection PyUnresolvedReferences
class StatusBar(QStatusBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statusBar")
        self.create_gui()
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.align_time_to_minute()

    def create_gui(self) -> None:
        self.time_label = QLabel()
        self.addPermanentWidget(self.time_label)

    def show_statusbar_message(self, message: str) -> None:
        self.showMessage(message, 5000)

    def update_time(self) -> None:
        current_time = QTime.currentTime().toString("HH:mm")
        self.time_label.setText(current_time)

    def align_time_to_minute(self) -> None:
        now = QTime.currentTime()
        msec_to_next_minute = (60 - now.second()) * 1000 - now.second()
        QTimer.singleShot(msec_to_next_minute, self.start_minute_timer)

    def start_minute_timer(self) -> None:
        self.update_time()
        self.timer.start(60 * 1000)