from typing import Callable

from PyQt6.QtCore import QThread, QObject, pyqtSignal


class BasicThread:
    def __init__(self):
        self.thread = None
        self.worker = None

    def run_basic_thread(self, worker: QObject, start_slot: Callable,
                         success_signal: pyqtSignal | None = None, success_callback: Callable | None = None,
                         on_error: Callable | None = None, on_finished: Callable | None = None) -> None:
        self.thread = QThread()
        self.worker = worker
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(start_slot)
        if success_signal and success_callback:
            success_signal.connect(success_callback)
        if on_error and hasattr(worker, "error_message"):
            worker.error_message.connect(on_error)
        if on_finished:
            worker.finished.connect(on_finished)
        worker.finished.connect(self.thread.quit)
        worker.finished.connect(worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
