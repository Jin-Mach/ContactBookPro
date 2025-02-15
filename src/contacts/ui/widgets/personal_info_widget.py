from PyQt6.QtWidgets import QWidget, QLayout, QHBoxLayout, QLabel, QFormLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class PersonalInfoWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("personalInfoWidget")
        self.parent = parent
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)
        self.contact_photo_label = QLabel()
        self.contact_photo_label.setObjectName("contactPhotoLabel")
        self.contact_photo_label.setFixedSize(150, 150)
        main_info_layout = QFormLayout()
        main_info_layout.setContentsMargins(0, 0, 0, 0)
        main_info_layout.setSpacing(5)
        self.contact_title_text_label = QLabel()
        self.contact_title_text_label.setObjectName("contactTitleTextLabel")
        self.contact_title_label = QLabel("ing")
        self.contact_title_label.setObjectName("contactTitleLabel")
        self.contact_first_name_text_label = QLabel()
        self.contact_first_name_text_label.setObjectName("contactFirstNameTextLabel")
        self.contact_first_name_label = QLabel("fisrt name")
        self.contact_first_name_label.setObjectName("contactFirstNameLabel")
        self.contact_second_name_text_label = QLabel()
        self.contact_second_name_text_label.setObjectName("contactSecondNameTextLabel")
        self.contact_second_name_label = QLabel("second name")
        self.contact_second_name_label.setObjectName("contactSecondNameLabel")
        self.contact_relationship_text_label = QLabel()
        self.contact_relationship_text_label.setObjectName("contactRelationshipTextLabel")
        self.contact_relationship_label = QLabel("family")
        self.contact_relationship_label.setObjectName("contactRelationshipLabel")
        self.contact_birthday_text_label = QLabel()
        self.contact_birthday_text_label.setObjectName("contactBirthdayTextLabel")
        self.contact_birthday_label = QLabel("1.1.2025")
        self.contact_birthday_label.setObjectName("contactBirthdayLabel")
        widgets = [(self.contact_title_text_label, self.contact_title_label),
            (self.contact_first_name_text_label, self.contact_first_name_label),
            (self.contact_second_name_text_label, self.contact_second_name_label),
            (self.contact_relationship_text_label, self.contact_relationship_label),
            (self.contact_birthday_text_label, self.contact_birthday_label)]
        for text_label, label in widgets:
            main_info_layout.addRow(text_label, label)
        main_layout.addWidget(self.contact_photo_label)
        main_layout.addLayout(main_info_layout)
        main_layout.addStretch()
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = [self.contact_title_text_label, self.contact_first_name_text_label, self.contact_second_name_text_label,
                   self.contact_relationship_text_label, self.contact_birthday_text_label]
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)