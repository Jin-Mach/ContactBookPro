import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QSystemTrayIcon

from src.application.status_bar import StatusBar
from src.contacts.ui.contacts_main_widget import ContactsMainWidget
from src.contacts.utilities.tray_icon import TrayIcon
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("mainWindow")
        self.setMinimumSize(1280, 720)
        self.showMaximized()
        self.setContentsMargins(0, 0, 0, 0)
        self.buttons_size = QSize(200, 50)
        self.icon_size = QSize(40, 40)
        self.contacts_main_widget = ContactsMainWidget(self)
        self.status_bar = StatusBar(self)
        self.setCentralWidget(self.create_gui())
        self.setStatusBar(self.status_bar)
        self.set_ui_text()
        self.set_tooltips_text()
        IconProvider.set_window_icon(self, self.objectName())
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QPushButton), self.buttons_size, self)
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = TrayIcon(self.status_bar, self)
            self.tray_icon.show()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        central_widget.setObjectName("mainWindowCentralWidget")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        dock_layout = QVBoxLayout()
        dock_layout.setContentsMargins(0,0,0,0)
        dock_layout.setSpacing(0)
        database_buttons_layout = QHBoxLayout()
        database_buttons_layout.setContentsMargins(0,0,0,0)
        database_buttons_layout.setSpacing(0)
        self.database_button = QPushButton()
        self.database_button.setObjectName("mainWindowDatabaseButton")
        self.database_button.setFixedSize(self.buttons_size)
        self.database_button.setFont(QFont("Arial", 12))
        self.database_button.setIconSize(self.icon_size)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("mainWindowStackedWidget")
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.addWidget(self.contacts_main_widget)
        self.stacked_widget.setCurrentWidget(self.contacts_main_widget)
        database_buttons_layout.addWidget(self.database_button)
        dock_layout.addWidget(MainWindow.create_image())
        dock_layout.addLayout(database_buttons_layout)
        dock_layout.addStretch()
        main_layout.addLayout(dock_layout)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            widgets = [self.database_button]
            if ui_text:
                if "mainWindowTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("mainWindowTitle", ""))
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            buttons = [self.database_button]
            if tooltips_text:
                for button in buttons:
                    if button.objectName() in tooltips_text:
                        button.setToolTip(tooltips_text[button.objectName()])
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def create_image() -> QLabel | None:
        icons_path = pathlib.Path(__file__).parents[2].joinpath("icons", "mainWindow")
        if icons_path.exists():
            pixmap = QPixmap(str(icons_path.joinpath("dog_image.png")))
            dock_image_label = QLabel()
            dock_image_label.setFixedSize(150, 150)
            dock_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dock_image_label.setObjectName("dockImageLabel")
            dock_image_label.setPixmap(pixmap.scaled(QSize(250, 250), Qt.AspectRatioMode.KeepAspectRatio,
                                                     Qt.TransformationMode.SmoothTransformation))
            return dock_image_label
        return None

    def closeEvent(self, event) -> None:
        pdf_path = pathlib.Path(__file__).parents[2].joinpath("output", "pdf_output.pdf")
        if pdf_path.exists():
            pdf_path.unlink()
        super().closeEvent(event)