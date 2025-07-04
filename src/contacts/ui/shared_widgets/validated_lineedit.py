from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QValidator
from PyQt6.QtWidgets import QLineEdit, QToolTip, QApplication

from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

control_keys = [Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down,
                Qt.Key.Key_Home, Qt.Key.Key_End, Qt.Key.Key_Tab, Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Escape]


class ValidatedLineedit(QLineEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("validatedLineedit")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.parent = parent
        self.tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
        self.error_text = LanguageProvider.get_error_text(self.objectName())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        try:
            if event.key() in control_keys or ((event.modifiers() & Qt.KeyboardModifier.ControlModifier)
                                               and event.key() in (Qt.Key.Key_C, Qt.Key.Key_X)):
                return super().keyPressEvent(event)
            validator = self.validator()
            if validator:
                if event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                    text = QApplication.clipboard().text()
                    if not text.strip():
                        if self.error_text:
                            DialogsProvider.show_error_dialog(self.error_text.get("emptyClipboard", ""), self.parent)
                        return None
                    if self.hasSelectedText():
                        selection_start = self.selectionStart()
                        selection_end = selection_start + len(self.selectedText())
                        new_text = self.text()[:selection_start] + text + self.text()[selection_end:]
                    else:
                        new_text = self.text()[:self.cursorPosition()] + text + self.text()[self.cursorPosition():]

                    status, _, _ = validator.validate(new_text, 0)
                    if status == QValidator.State.Invalid:
                        if self.tooltips_text:
                            QToolTip.showText(self.mapToGlobal(self.cursorRect().bottomRight()),
                                              f'{self.tooltips_text.get("invalidChar", "")} "{text}"',
                                              self, msecShowTime=2000)
                        return None
                else:
                    if self.hasSelectedText():
                        selection_start = self.selectionStart()
                        selection_end = selection_start + len(self.selectedText())
                        prepared_text = self.text()[:selection_start] + event.text() + self.text()[selection_end:]
                    else:
                        prepared_text = self.text()[:self.cursorPosition()] + event.text() + self.text()[
                                                                                             self.cursorPosition():]

                    status, _, _ = validator.validate(prepared_text, 0)
                    if status == QValidator.State.Invalid:
                        if self.tooltips_text:
                            QToolTip.showText(self.mapToGlobal(self.cursorRect().bottomRight()),
                                              f'{self.tooltips_text.get("invalidChar", "")} "{event.text()}"',
                                              self, msecShowTime=2000)
                        return None
            return super().keyPressEvent(event)

        except Exception as e:
            ErrorHandler.exception_handler(e, self)