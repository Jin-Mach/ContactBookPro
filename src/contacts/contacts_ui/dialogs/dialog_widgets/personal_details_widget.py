from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QWidget, QLayout, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFormLayout,
                             QLineEdit, QTextEdit)

from src.contacts.contacts_ui.dialogs.calendar_dialog import CalendarDialog
from src.contacts.contacts_utilities.image_blob_handler import image_to_blob
from src.contacts.contacts_utilities.notes_ulitities import check_notes_length
from src.contacts.contacts_utilities.photo_utilities import set_contact_photo, reset_contact_photo
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
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QPushButton), self.button_size, self)
        self.reset_photo_label()

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
        self.dialog_title_edit = QLineEdit()
        self.dialog_title_edit.setObjectName("dialogTitleEdit")
        self.dialog_title_edit.setFixedWidth(200)
        self.dialog_birthday_text_label = QLabel()
        self.dialog_birthday_text_label.setObjectName("dialogBirthdayTextLabel")
        self.dialog_birthday_edit = QLineEdit()
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
        self.dialog_notes_edit.textChanged.connect(lambda: check_notes_length(self.dialog_notes_edit, self.dialog_letters_count_label, self))
        letters_count_layout = QHBoxLayout()
        self.dialog_letters_count_label = QLabel("0/500")
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
        ui_text = LanguageProvider.get_dialog_text(self.objectName())
        widgets = [self.dialog_title_text_label, self.dialog_birthday_text_label, self.dialog_notes_edit]
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(ui_text[widget.objectName()])
                    elif isinstance(widget, QTextEdit):
                        widget.setPlaceholderText(ui_text[widget.objectName()])
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

    def return_personal_data(self) -> Optional[list]:
        inputs = self.findChildren((QLineEdit, QTextEdit))
        inputs_names = ["dialogTitleEdit", "dialogBirthdayEdit", "dialogNotesEdit"]
        photo_blob = image_to_blob(self.dialog_photo_label, self)
        personal_data = []
        try:
            for widget in inputs:
                if widget.objectName() in inputs_names:
                    if isinstance(widget, QLineEdit):
                        personal_data.append(str(widget.text().strip()))
                    elif isinstance(widget, QTextEdit):
                        personal_data.append(widget.toPlainText().strip())
            if self.photo_state == 1:
                personal_data.append(photo_blob)
            else:
                personal_data.append(None)
            return personal_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None