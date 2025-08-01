import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QSystemTrayIcon, QFrame

from src.application.main_window_widgets.button_widget import MainWindowButtonWidget
from src.application.status_bar import StatusBar
from src.contacts.ui.contacts_main_widget import ContactsMainWidget
from src.contacts.utilities.tray_icon import TrayIcon
from src.database.db_connection import create_db_connection
from src.database.models.mandatory_model import MandatoryModel
from src.map.ui.map_main_widget import MapMainWidget
from src.statistics.ui.statistics_main_widget import StatisticsMainWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger
from src.utilities.messagebox_provider import MessageboxProvider
from src.utilities.settings_provider import SettingsProvider


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("mainWindow")
        self.setMinimumSize(1280, 720)
        self.showMaximized()
        self.setContentsMargins(0, 0, 0, 0)
        self.icon_size = QSize(30, 30)
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        db_connection = create_db_connection("contacts_db.sqlite")
        mandatory_model = MandatoryModel(db_connection)
        self.map_main_widget = MapMainWidget(db_connection, self.status_bar, self)
        self.statistics_main_widget = StatisticsMainWidget(db_connection, mandatory_model, self.status_bar, self)
        self.contacts_main_widget = ContactsMainWidget(db_connection, mandatory_model, self,
                                                       self.map_main_widget.map_controller, self.statistics_main_widget.statistics_controller)
        self.setCentralWidget(self.create_gui())
        self.set_icons()
        self.set_ui_text()
        self.set_tooltips_text()
        IconProvider.set_window_icon(self, self.objectName())
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = TrayIcon(self.status_bar, self)
            self.tray_icon.show()
        SettingsProvider.load_settings(self, QSize(1280, 720))

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        central_widget.setObjectName("mainWindowCentralWidget")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        dock_frame = QFrame()
        dock_frame.setObjectName("mainWindowDockFrame")
        dock_frame.setStyleSheet(self.set_frame_style())
        dock_layout = QVBoxLayout(dock_frame)
        dock_layout.setContentsMargins(0,0,0,0)
        dock_layout.setSpacing(0)
        database_buttons_layout = QVBoxLayout()
        database_buttons_layout.setContentsMargins(0,0,0,0)
        database_buttons_layout.setSpacing(10)
        self.database_button = MainWindowButtonWidget(lambda: self.changed_stack(0), self)
        self.database_button.setObjectName("mainWindowDatabaseButton")
        self.map_button = MainWindowButtonWidget(lambda: self.changed_stack(1), self)
        self.map_button.setObjectName("mainWindowMapButton")
        self.statistics_button = MainWindowButtonWidget(lambda: self.changed_stack(2), self)
        self.statistics_button.setObjectName("mainWindowStatisticsButton")
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("mainWindowStackedWidget")
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.addWidget(self.contacts_main_widget)
        self.stacked_widget.addWidget(self.map_main_widget)
        self.stacked_widget.addWidget(self.statistics_main_widget)
        self.stacked_widget.setCurrentWidget(self.contacts_main_widget)
        database_buttons_layout.addWidget(self.database_button)
        database_buttons_layout.addWidget(self.map_button)
        database_buttons_layout.addWidget(self.statistics_button)
        dock_layout.addWidget(MainWindow.create_image())
        dock_layout.addLayout(database_buttons_layout)
        dock_layout.addStretch()
        dock_frame.setLayout(dock_layout)
        main_layout.addWidget(dock_frame)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def set_icons(self) -> None:
        try:
            buttons = [self.database_button, self.map_button, self.statistics_button]
            for button in buttons:
                if button.objectName().endswith("Button"):
                    button.set_label_icon(button.objectName())
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_ui_text(self) -> None:
        try:
            self.ui_text = LanguageProvider.get_ui_text(self.objectName())
            buttons = [self.database_button, self.map_button, self.statistics_button]
            if self.ui_text:
                if "mainWindowTitle" in self.ui_text:
                    self.setWindowTitle(self.ui_text.get("mainWindowTitle", ""))
                for button in buttons:
                    if button.objectName().endswith("Button") and button.objectName() in self.ui_text:
                        button.set_text(self.ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            buttons = [self.database_button, self.map_button, self.statistics_button]
            if tooltips_text:
                for button in buttons:
                    if button.objectName().endswith("Button") and button.objectName() in tooltips_text:
                        button.setToolTip(tooltips_text[button.objectName()])
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def create_image() -> QLabel | None:
        try:
            icons_path = pathlib.Path(__file__).parents[2].joinpath("icons", "mainWindow")
            dock_image_label = QLabel()
            dock_image_label.setFixedSize(150, 150)
            dock_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dock_image_label.setObjectName("dockImageLabel")
            if icons_path.exists():
                pixmap = QPixmap(str(icons_path.joinpath("mainWindowLogo.png")))
                dock_image_label.setPixmap(pixmap.scaled(QSize(100, 100), Qt.AspectRatioMode.KeepAspectRatio,
                                                         Qt.TransformationMode.SmoothTransformation))
            return dock_image_label
        except Exception as e:
            ErrorHandler.exception_handler(e, MainWindow)
            return None

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            result = MessageboxProvider.close_application_messagebox(self.ui_text, self)
            if not result:
                event.ignore()
            else:
                pdf_path = pathlib.Path(__file__).parents[2].joinpath("output", "pdf_output.pdf")
                if pdf_path.exists():
                    pdf_path.unlink()
                SettingsProvider.save_settings(self)
                event.accept()
        except Exception as e:
            logger = get_logger()
            logger.error(f"{self.__class__.__name__}: {e}", exc_info=True)

    def changed_stack(self, index: int) -> None:
        if index == 2:
            self.statistics_main_widget.statistics_tab_widget.setCurrentIndex(0)
        self.stacked_widget.setCurrentIndex(index)

    @staticmethod
    def set_frame_style() -> str:
        return """
            QFrame#mainWindowDockFrame {
                border-right: 1px solid #448aff;
                background-color: #1e1e2f;
            }
        """