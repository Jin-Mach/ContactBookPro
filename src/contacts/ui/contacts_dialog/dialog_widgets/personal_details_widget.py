from PyQt6.QtCore import QSize, Qt, QByteArray
from PyQt6.QtWidgets import (QWidget, QLayout, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFormLayout,
                             QLineEdit, QTextEdit)

from src.contacts.ui.contacts_dialog.calendar_dialog import CalendarDialog
from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineEdit
from src.contacts.utilities.blob_handler import BlobHandler
from src.contacts.utilities.check_update_data import CheckUpdateProvider
from src.contacts.utilities.contact_validator import ContactValidator
from src.contacts.utilities.notes_utilities import check_notes_length
from src.contacts.utilities.optimalize_data import normalize_texts
from src.contacts.utilities.photo_utilities import set_contact_photo, reset_contact_photo
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class PersonalDetailsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogPersonalDetailWidget")
        self.button_size = QSize(35, 35)
        self.photo_label_size = QSize(150, 150)
        self.photo_state = 0
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.set_tooltips_text()
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QPushButton), self.button_size, self)
        self.reset_photo_label()
        ContactValidator.contact_input_validator(title_edit=self.dialog_title_edit)
        self.default_data = None

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        photo_layout = QVBoxLayout()
        photo_label_layout = QHBoxLayout()
        photo_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dialog_photo_label = QLabel()
        self.dialog_photo_label.setObjectName("dialogPhotoLabel")
        self.dialog_photo_label.setFixedSize(self.photo_label_size)
        photo_buttons_layout = QHBoxLayout()
        self.dialog_get_photo_pushbutton = QPushButton()
        self.dialog_get_photo_pushbutton.setObjectName("dialogGetPhotoPushbutton")
        self.dialog_get_photo_pushbutton.clicked.connect(self.set_custom_image_photo_label)
        self.dialog_reset_photo_button = QPushButton()
        self.dialog_reset_photo_button.setObjectName("dialogResetPhotoButton")
        self.dialog_reset_photo_button.clicked.connect(self.reset_photo_label)
        title_date_container = QHBoxLayout()
        title_date_layout = QFormLayout()
        self.dialog_title_text_label = QLabel()
        self.dialog_title_text_label.setObjectName("dialogTitleTextLabel")
        self.dialog_title_edit = ValidatedLineEdit(self)
        self.dialog_title_edit.setObjectName("dialogTitleEdit")
        self.dialog_title_edit.setFixedWidth(200)
        self.dialog_birthday_text_label = QLabel()
        self.dialog_birthday_text_label.setObjectName("dialogBirthdayTextLabel")
        self.dialog_birthday_edit = ValidatedLineEdit(self)
        self.dialog_birthday_edit.setObjectName("dialogBirthdayEdit")
        self.dialog_birthday_edit.setFixedWidth(200)
        self.dialog_birthday_edit.setReadOnly(True)
        calendar_buttons_widget = QWidget()
        calendar_buttons_widget.setFixedWidth(200)
        calendar_buttons_layout = QHBoxLayout()
        calendar_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.dialog_calendar_pushbutton = QPushButton()
        self.dialog_calendar_pushbutton.setObjectName("dialogCalendarPushbutton")
        self.dialog_calendar_pushbutton.clicked.connect(self.get_birthday_date)
        self.dialog_reset_calendar_pushbutton = QPushButton()
        self.dialog_reset_calendar_pushbutton.setObjectName("dialogResetCalendarPushbutton")
        self.dialog_reset_calendar_pushbutton.clicked.connect(self.dialog_birthday_edit.clear)
        notes_layout = QVBoxLayout()
        self.dialog_notes_edit = QTextEdit()
        self.dialog_notes_edit.setObjectName("dialogNotesEdit")
        self.dialog_notes_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.dialog_notes_edit.textChanged.connect(lambda: check_notes_length(self.dialog_notes_edit, self.dialog_letters_count_label, self))
        letters_count_layout = QHBoxLayout()
        self.dialog_letters_count_label = QLabel("0/200")
        self.dialog_letters_count_label.setObjectName("dialogLettersCountLabel")
        photo_buttons_layout.addWidget(self.dialog_get_photo_pushbutton)
        photo_buttons_layout.addWidget(self.dialog_reset_photo_button)
        photo_label_layout.addWidget(self.dialog_photo_label)
        photo_layout.addLayout(photo_label_layout)
        photo_layout.addLayout(photo_buttons_layout)
        calendar_buttons_layout.addWidget(self.dialog_calendar_pushbutton)
        calendar_buttons_layout.addWidget(self.dialog_reset_calendar_pushbutton)
        calendar_buttons_widget.setLayout(calendar_buttons_layout)
        title_date_layout.addRow(self.dialog_title_text_label, self.dialog_title_edit)
        title_date_layout.addRow(self.dialog_birthday_text_label, self.dialog_birthday_edit)
        title_date_layout.addRow(None, calendar_buttons_widget)
        title_date_container.addStretch()
        title_date_container.addLayout(title_date_layout)
        letters_count_layout.addStretch()
        letters_count_layout.addWidget(self.dialog_letters_count_label)
        notes_layout.addWidget(self.dialog_notes_edit)
        notes_layout.addLayout(letters_count_layout)
        main_layout.addLayout(photo_layout, 0, 0)
        main_layout.addLayout(title_date_container, 0, 1)
        main_layout.addLayout(notes_layout, 1, 0, 1, 2)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_dialog_text(self.objectName())
            widgets = self.findChildren((QLabel, QLineEdit, QTextEdit))
            if ui_text:
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(ui_text.get(widget.objectName(), ""))
                        elif isinstance(widget, (QLineEdit, QTextEdit)):
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            buttons = self.findChildren(QPushButton)
            if tooltips_text:
                for button in buttons:
                    if button.objectName() in tooltips_text:
                        button.setToolTip(tooltips_text.get(button.objectName(), ""))
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_custom_image_photo_label(self) -> None:
        set_contact_photo(self.dialog_photo_label, self.photo_label_size, self)
        self.photo_state = 1

    def reset_photo_label(self) -> None:
        reset_contact_photo(self.dialog_photo_label, self.photo_label_size, self)
        self.photo_state = 0

    def get_birthday_date(self) -> str:
        try:
            dialog = CalendarDialog(self.dialog_birthday_edit, self)
            if dialog.exec() == dialog.DialogCode.Accepted:
                result = dialog.return_date(self.dialog_birthday_edit)
                if result:
                    return result
            return ""
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return ""

    def return_personal_data(self) -> list | None:
        try:
            inputs = self.findChildren((QLineEdit, QTextEdit))
            inputs_names = ["dialogTitleEdit", "dialogBirthdayEdit", "dialogNotesEdit"]
            photo_blob = BlobHandler.pixmap_to_blob(self.dialog_photo_label, self)
            personal_data = []
            for widget in inputs:
                if widget.objectName() in inputs_names:
                    if isinstance(widget, QLineEdit):
                        personal_data.append(str(widget.text().strip()))
                    elif isinstance(widget, QTextEdit):
                        personal_data.append(widget.toPlainText().strip())
            if self.photo_state == 1 and isinstance(photo_blob, bytes):
                personal_data.append(photo_blob)
            else:
                personal_data.append(None)
            personal_data += normalize_texts([self.dialog_title_edit, self.dialog_notes_edit])
            if self.default_data:
                return [personal_data, CheckUpdateProvider.check_update(self.objectName(), self.default_data, personal_data)]
            return personal_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def set_contact_data(self, data: dict) -> None:
        try:
            widget_data = [data.get("title", ""), data.get("birthday", ""), data.get("notes", ""), data.get("photo", None)]
            self.default_data = widget_data
            self.dialog_title_edit.setText(widget_data[0])
            self.dialog_birthday_edit.setText(widget_data[1])
            self.dialog_notes_edit.setPlainText(widget_data[2])
            if widget_data[3] is not None:
                self.set_photo_pixmap(widget_data[3], self.dialog_photo_label)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_photo_pixmap(self, blob: QByteArray | None, label: QLabel) -> None:
        try:
            pixmap = BlobHandler.blob_to_pixmap(blob, self)
            if pixmap:
                label.setPixmap(pixmap)
                self.photo_state = 1
            else:
                self.photo_state = 0
        except Exception as e:
            ErrorHandler.exception_handler(e, self)