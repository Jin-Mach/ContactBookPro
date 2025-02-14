import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from src.contacts.ui.contacts_main_widget import ContactsMainWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("mainWindow")
        self.setMinimumSize(1280, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons")
        self.buttons_size = QSize(150, 50)
        self.icon_size = QSize(40, 40)
        self.contacts_main_widget = ContactsMainWidget()
        self.setCentralWidget(self.create_gui())
        self.set_ui_text()
        self.test()

    def test(self):
        try:
            1/0
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def create_image(self) -> QLabel:
        pixmap = QPixmap(str(self.icons_path.joinpath("no_image.png")))
        dock_image_label = QLabel()
        dock_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dock_image_label.setObjectName("dockImageLabel")
        dock_image_label.setPixmap(pixmap.scaled(QSize(150, 150), Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation))
        return dock_image_label

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
        self.database_button.setIcon(QIcon(str(self.icons_path.joinpath("database_icon.png"))))
        self.database_button.setIconSize(self.icon_size)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("mainWindowStackedWidget")
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.addWidget(self.contacts_main_widget)
        self.stacked_widget.setCurrentWidget(self.contacts_main_widget)
        database_buttons_layout.addWidget(self.database_button)
        dock_layout.addWidget(self.create_image())
        dock_layout.addLayout(database_buttons_layout)
        dock_layout.addStretch()
        main_layout.addLayout(dock_layout)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text("mainWindow")
        self.setWindowTitle(ui_text[f"{self.objectName()}Title"])
        self.database_button.setText(ui_text[self.database_button.objectName()])