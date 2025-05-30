from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QApplication


def get_main_window_instance() -> Optional[QMainWindow]:
    application = QApplication.instance()
    if application is None:
        return None
    main_window = getattr(application, "main_window", None)
    if main_window:
        if isinstance(main_window, QMainWindow):
            return main_window
    return None