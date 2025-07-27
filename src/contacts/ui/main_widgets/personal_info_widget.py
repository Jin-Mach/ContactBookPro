import pathlib

from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFormLayout, QTabWidget

from src.contacts.utilities.blob_handler import BlobHandler
from src.contacts.utilities.date_handler import format_date
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class PersonalTabInfoWidget(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("personalTabInfoWidget")
        self.setFixedWidth(400)
        self.addTab(self.create_gui(), "")
        self.ui_text = LanguageProvider.get_ui_text(self.objectName())
        self.set_ui_text()

    def create_gui(self) -> QWidget:
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.contact_title_label = QLabel()
        self.contact_title_label.setObjectName("contactTitleLabel")
        self.contact_gender_text_label = QLabel()
        self.contact_gender_text_label.setObjectName("contactGenderTextLabel")
        self.contact_gender_label = QLabel()
        self.contact_gender_label.setObjectName("contactGenderLabel")
        self.contact_first_name_text_label = QLabel()
        self.contact_first_name_text_label.setObjectName("contactFirstNameTextLabel")
        self.contact_first_name_label = QLabel()
        self.contact_first_name_label.setObjectName("contactFirstNameLabel")
        self.contact_second_name_text_label = QLabel()
        self.contact_second_name_text_label.setObjectName("contactSecondNameTextLabel")
        self.contact_second_name_label = QLabel()
        self.contact_second_name_label.setObjectName("contactSecondNameLabel")
        self.contact_relationship_text_label = QLabel()
        self.contact_relationship_text_label.setObjectName("contactRelationshipTextLabel")
        self.contact_relationship_label = QLabel()
        self.contact_relationship_label.setObjectName("contactRelationshipLabel")
        self.contact_birthday_text_label = QLabel()
        self.contact_birthday_text_label.setObjectName("contactBirthdayTextLabel")
        self.contact_birthday_label = QLabel()
        self.contact_birthday_label.setObjectName("contactBirthdayLabel")
        widgets = [(self.contact_title_text_label, self.contact_title_label),
                   (self.contact_gender_text_label, self.contact_gender_label),
            (self.contact_first_name_text_label, self.contact_first_name_label),
            (self.contact_second_name_text_label, self.contact_second_name_label),
            (self.contact_relationship_text_label, self.contact_relationship_label),
            (self.contact_birthday_text_label, self.contact_birthday_label)]
        for text_label, label in widgets:
            main_info_layout.addRow(text_label, label)
        main_layout.addWidget(self.contact_photo_label)
        main_layout.addLayout(main_info_layout)
        main_layout.addStretch()
        main_widget.setLayout(main_layout)
        return main_widget

    def set_ui_text(self) -> None:
        try:
            widgets = [self, self.contact_title_text_label, self.contact_gender_text_label,
                       self.contact_first_name_text_label,
                       self.contact_second_name_text_label, self.contact_relationship_text_label,
                       self.contact_birthday_text_label]
            if self.ui_text:
                for widget in widgets:
                    if widget.objectName() in self.ui_text or f"{widget.objectName()}_tabText" in self.ui_text:
                        if isinstance(widget, QTabWidget):
                            widget.setTabText(0, self.ui_text.get(f"{widget.objectName()}_tabText", ""))
                        elif isinstance(widget, QLabel):
                            widget.setText(self.ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_data(self, data: dict) -> None:
        try:
            if self.ui_text:
                gender_dict = self.ui_text.get("gender_key", {})
                relationship_dict = self.ui_text.get("relationship_key", {})
                self.set_photo_pixmap(data.get("photo"), int(data.get("gender", 0)))
                self.contact_title_label.setText(data.get("title", ""))
                self.contact_gender_label.setText(gender_dict.get(str(data.get("gender", "")), ""))
                self.contact_first_name_label.setText(data.get("first_name", ""))
                self.contact_second_name_label.setText(data.get("second_name", ""))
                self.contact_relationship_label.setText(relationship_dict.get(str(data.get("relationship", "")), ""))
                iso_date = data.get("birthday", "")
                self.contact_birthday_label.setText(format_date(iso_date))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def reset_data(self) -> None:
        labels = self.findChildren(QLabel)
        for label in labels:
            if not label.objectName().endswith("TextLabel"):
                label.clear()

    def set_photo_pixmap(self, blob: QByteArray, gender: int) -> None:
        try:
            pixmap = BlobHandler.blob_to_pixmap(blob, self)
            if not pixmap:
                male_icon_path = pathlib.Path(__file__).parents[4].joinpath("icons", "personalTabInfoWidget",
                                                                            "male_icon.png")
                female_icon_path = pathlib.Path(__file__).parents[4].joinpath("icons", "personalTabInfoWidget",
                                                                              "female_icon.png")
                if gender == 1 and male_icon_path.exists():
                    pixmap = QPixmap(str(male_icon_path))
                    self.contact_photo_label.setPixmap(pixmap)
                elif gender == 2 and female_icon_path.exists():
                    pixmap = QPixmap(str(female_icon_path))
                    self.contact_photo_label.setPixmap(pixmap)
            else:
                self.contact_photo_label.setPixmap(pixmap)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)