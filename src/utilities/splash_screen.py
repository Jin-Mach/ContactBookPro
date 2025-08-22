import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSplashScreen, QApplication

from src.utilities.logger_provider import get_logger


class SplashScreen(QSplashScreen):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("splashScreen")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setFixedSize(500, 250)
        self.create_gui()
        self.center_on_screen()

    def create_gui(self) -> None:
        logger = get_logger()
        try:
            icon_path = pathlib.Path(__file__).parents[2].joinpath("icons", "splashScreen", "splash_icon.png")
            if not icon_path.exists():
                logger.error(f"{self.__class__.__name__}: Icon not found at {icon_path}")
                self.setStyleSheet("font-family: Tahoma; font-size: 20pt;")
                self.showMessage("Contact Book Pro...", Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
                                 Qt.GlobalColor.black)
            else:
                pixmap = QPixmap(str(icon_path))
                pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
                self.setPixmap(pixmap)
                self.setStyleSheet("font-family: Tahoma; font-size: 20pt;")
                self.showMessage("Contact Book Pro...", Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
                                 Qt.GlobalColor.black)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}", exc_info=True)
            self.close()

    def center_on_screen(self) -> None:
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            splash_size = self.size()
            x = (screen_geometry.width() - splash_size.width()) // 2
            y = (screen_geometry.height() - splash_size.height()) // 2
            self.move(x, y)