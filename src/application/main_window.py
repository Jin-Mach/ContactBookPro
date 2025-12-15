import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QSystemTrayIcon, QFrame, QSizePolicy

from src.about.about_application_dialog import AboutApplicationDialog
from src.application.main_window_widgets.main_window_button_widget import MainWindowButtonWidget
from src.application.status_bar import StatusBar
from src.application.utilities.holidays_checker import get_local_holidays
from src.contacts.ui.contacts_main_widget import ContactsMainWidget
from src.contacts.utilities.tray_icon import TrayIcon
from src.database.db_connection import create_db_connection
from src.database.models.mandatory_model import MandatoryModel
from src.manual.ui.manual_main_widget import ManualMainWidget
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
        self.setContentsMargins(0, 0, 0, 0)
        self.icon_size = QSize(30, 30)
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        db_connection = create_db_connection("contacts_db.sqlite")
        mandatory_model = MandatoryModel(db_connection, self)
        self.map_main_widget = MapMainWidget(db_connection, mandatory_model, self.status_bar, self)
        self.statistics_main_widget = StatisticsMainWidget(db_connection, mandatory_model, self.status_bar, self)
        self.contacts_main_widget = ContactsMainWidget(db_connection, mandatory_model, self,
                                                       self.map_main_widget.map_controller, self.statistics_main_widget.statistics_controller)
        self.manual_main_widget = ManualMainWidget(self)
        self.setCentralWidget(self.create_gui())
        self.buttons = [self.database_button, self.map_button, self.statistics_button, self.manual_button, self.about_button]
        self.set_icons()
        self.set_ui_text()
        self.set_tooltips_text()
        IconProvider.set_window_icon(self, self.objectName())
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = TrayIcon(self.status_bar, self)
            self.tray_icon.show()
        SettingsProvider.load_settings(self)
        self.set_holidays_button()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        central_widget.setObjectName("mainWindowCentralWidget")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        dock_frame = QFrame()
        dock_frame.setObjectName("mainWindowDockFrame")
        dock_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        dock_frame.setStyleSheet("""
            QFrame#mainWindowDockFrame {
                border-right: 1px solid #448aff;
                background-color: #1e1e2f;
            }
        """)
        dock_layout = QVBoxLayout(dock_frame)
        dock_layout.setContentsMargins(0, 0, 0, 10)
        dock_layout.setSpacing(0)
        database_buttons_layout = QVBoxLayout()
        database_buttons_layout.setContentsMargins(0, 0, 0, 0)
        database_buttons_layout.setSpacing(5)
        self.database_button = MainWindowButtonWidget(lambda: self.changed_stack(0), self)
        self.database_button.setObjectName("mainWindowDatabaseButton")
        self.map_button = MainWindowButtonWidget(lambda: self.changed_stack(1), self)
        self.map_button.setObjectName("mainWindowMapButton")
        self.statistics_button = MainWindowButtonWidget(lambda: self.changed_stack(2), self)
        self.statistics_button.setObjectName("mainWindowStatisticsButton")
        self.manual_button = MainWindowButtonWidget(lambda: self.changed_stack(3), self)
        self.manual_button.setObjectName("mainWindowManualButton")
        self.about_button = MainWindowButtonWidget(lambda: self.changed_stack(4), self)
        self.about_button.setObjectName("mainWindowAboutButton")
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("mainWindowStackedWidget")
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.addWidget(self.contacts_main_widget)
        self.stacked_widget.addWidget(self.map_main_widget)
        self.stacked_widget.addWidget(self.statistics_main_widget)
        self.stacked_widget.addWidget(self.manual_main_widget)
        self.stacked_widget.setCurrentWidget(self.contacts_main_widget)
        database_buttons_layout.addWidget(self.database_button)
        database_buttons_layout.addWidget(self.map_button)
        database_buttons_layout.addWidget(self.statistics_button)
        database_buttons_layout.addStretch()
        database_buttons_layout.addWidget(self.manual_button)
        database_buttons_layout.addWidget(self.about_button)
        dock_layout.addWidget(MainWindow.create_image())
        dock_layout.addLayout(database_buttons_layout)
        dock_frame.setLayout(dock_layout)
        main_layout.addWidget(dock_frame)
        main_layout.addWidget(self.stacked_widget, 1)
        central_widget.setLayout(main_layout)
        return central_widget

    def set_icons(self) -> None:
        try:
            for button in self.buttons:
                if button.objectName().endswith("Button"):
                    button.set_label_icon(button.objectName())
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_ui_text(self) -> None:
        try:
            self.ui_text = LanguageProvider.get_json_text("ui_text.json", self.objectName())
            if self.ui_text:
                if "mainWindowTitle" in self.ui_text:
                    self.setWindowTitle(self.ui_text.get("mainWindowTitle", ""))
                for button in self.buttons:
                    if button.objectName().endswith("Button") and button.objectName() in self.ui_text:
                        button.set_text(self.ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_json_text("tooltips_text.json", self.objectName())
            if tooltips_text:
                for button in self.buttons:
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
        elif index == 3:
           self.manual_main_widget.set_manual_widget_to_default()
        elif index == 4:
            dialog = AboutApplicationDialog(self)
            dialog.exec()
        self.stacked_widget.setCurrentIndex(index)

    def set_holidays_button(self) -> None:
        self.holiday_data = get_local_holidays()
        if self.holiday_data:
            self.status_bar.holidays_label.setVisible(False)
            self.status_bar.holidays_button.setStyleSheet(
            "border: 2px solid #FF9999;"
            "border-radius: 5px;"
            "padding: 2px;"
            )
            self.status_bar.set_tooltips_text()
            self.status_bar.holidays_button.setVisible(True)
        else:
            self.status_bar.holidays_label.setVisible(True)
            self.status_bar.holidays_button.setStyleSheet("")
            self.status_bar.holidays_button.setVisible(False)