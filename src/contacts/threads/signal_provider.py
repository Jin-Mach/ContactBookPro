from PyQt6.QtCore import QObject, pyqtSignal


class SignalProvider(QObject):
        contact_coordinates = pyqtSignal(int, tuple)