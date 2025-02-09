from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit, \
    QFormLayout, QLineEdit

from src.utilities.language_provider import LanguageProvider


class PersonalDetailsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogPersonalDetailWidget")
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        photo_layout = QVBoxLayout()
        self.dialog_photo_label = QLabel()
        self.dialog_photo_label.setObjectName("dialogPhotoLabel")
        self.dialog_photo_label.setFixedSize(150, 150)
        photo_buttons_layout = QHBoxLayout()
        self.dialog_get_photo_pushbutton = QPushButton()
        self.dialog_get_photo_pushbutton.setObjectName("dialogGetPhotoPushbutton")
        self.dialog_reset_photo_button = QPushButton()
        self.dialog_reset_photo_button.setObjectName("dialogResetPhotoButton")
        title_date_layout = QFormLayout()
        self.dialog_title_text_label = QLabel()
        self.dialog_title_text_label.setObjectName("dialogTitleTextLabel")
        self.dialog_title_edit = QLineEdit()
        self.dialog_title_edit.setObjectName("dialogTitleEdit")
        self.dialog_birthday_text_label = QLabel()
        self.dialog_birthday_text_label.setObjectName("dialogBirthdayTextLabel")
        self.dialog_birthday_edit = QLineEdit()
        self.dialog_birthday_edit.setObjectName("dialogBirthdayEdit")
        self.dialog_birthday_edit.setReadOnly(True)
        calendar_buttons_layout = QHBoxLayout()
        self.dialog_calendar_pushbutton = QPushButton()
        self.dialog_calendar_pushbutton.setObjectName("dialogCalendarPushbutton")
        self.dialog_reset_calendar_pushbutton = QPushButton()
        self.dialog_reset_calendar_pushbutton.setObjectName("dialogResetCalendarPushbutton")
        notes_layout = QVBoxLayout()
        self.dialog_notes_edit = QTextEdit()
        self.dialog_notes_edit.setObjectName("dialogNotesEdit")
        letters_count_layout = QHBoxLayout()
        self.dialog_letters_count_label = QLabel("0/500")
        self.dialog_letters_count_label.setObjectName("dialogLettersCountLabel")
        photo_buttons_layout.addWidget(self.dialog_get_photo_pushbutton)
        photo_buttons_layout.addWidget(self.dialog_reset_photo_button)
        photo_layout.addWidget(self.dialog_photo_label)
        photo_layout.addLayout(photo_buttons_layout)
        calendar_buttons_layout.addWidget(self.dialog_calendar_pushbutton)
        calendar_buttons_layout.addWidget(self.dialog_reset_calendar_pushbutton)
        title_date_layout.addRow(self.dialog_title_text_label, self.dialog_title_edit)
        title_date_layout.addRow(self.dialog_birthday_text_label, self.dialog_birthday_edit)
        title_date_layout.addRow(None, calendar_buttons_layout)
        letters_count_layout.addStretch()
        letters_count_layout.addWidget(self.dialog_letters_count_label)
        notes_layout.addWidget(self.dialog_notes_edit)
        notes_layout.addLayout(letters_count_layout)
        main_layout.addLayout(photo_layout, 0, 0)
        main_layout.addLayout(title_date_layout, 0, 1)
        main_layout.addLayout(notes_layout, 1, 0, 1, 2)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = [self.dialog_get_photo_pushbutton, self.dialog_reset_photo_button, self.dialog_title_text_label,
                   self.dialog_birthday_text_label, self.dialog_calendar_pushbutton, self.dialog_reset_calendar_pushbutton,
                   self.dialog_notes_edit]
        for widget in widgets:
            if widget.objectName() in ui_text:
                if isinstance(widget, (QLabel, QPushButton)):
                    widget.setText(ui_text[widget.objectName()])
                if isinstance(widget, QTextEdit):
                    widget.setPlaceholderText(ui_text[widget.objectName()])
            else:
                print("error")