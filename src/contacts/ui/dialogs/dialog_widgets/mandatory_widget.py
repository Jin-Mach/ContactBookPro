from PyQt6.QtWidgets import QWidget, QLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, \
    QPushButton


class MandatoryWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogMandatoryWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.dialog_first_name_text_label = QLabel("first name:")
        self.dialog_first_name_text_label.setObjectName("dialogFirstNameTextLabel")
        self.dialog_first_name_edit = QLineEdit()
        self.dialog_first_name_edit.setObjectName("dialogFirstNameEdit")
        self.dialog_second_name_text_label = QLabel("second name:")
        self.dialog_second_name_text_label.setObjectName("dialogSecondNameTextLabel")
        self.dialog_second_name_edit = QLineEdit()
        self.dialog_second_name_edit.setObjectName("dialogSecondNameEdit")
        self.dialog_relationship_text_label = QLabel("relation:")
        self.dialog_relationship_text_label.setObjectName("dialogRelationshipTextLabel")
        self.dialog_relationship_combobox = QComboBox()
        self.dialog_relationship_combobox.setObjectName("dialogRelationshipCombobox")
        self.dialog_relationship_combobox.setFixedWidth(200)
        self.dialog_email_text_label = QLabel("email:")
        self.dialog_email_text_label.setObjectName("dialogEmailTextLabel")
        self.dialog_email_edit = QLineEdit()
        self.dialog_email_edit.setObjectName("dialogEmailEdit")
        self.dialog_phone_number_text_label = QLabel("phone:")
        self.dialog_phone_number_text_label.setObjectName("dialogPhoneNumberTextLabel")
        self.dialog_phone_number_edit = QLineEdit()
        self.dialog_phone_number_edit.setObjectName("dialogPhoneNumberEdit")
        self.dialog_address_text_label = QLabel("address:")
        self.dialog_address_text_label.setObjectName("dialogAddressTextLabel")
        self.dialog_address_edit = QLineEdit()
        self.dialog_address_edit.setObjectName("dialogAddressEdit")
        self.dialog_city_text_label = QLabel("city:")
        self.dialog_city_text_label.setObjectName("dialogCityTextLabel")
        self.dialog_city_edit = QLineEdit()
        self.dialog_city_edit.setObjectName("dialogCityEdit")
        self.dialog_post_code_text_label = QLabel("post code:")
        self.dialog_post_code_text_label.setObjectName("dialogPostCodeTextLabel")
        self.dialog_post_code_edit = QLineEdit()
        self.dialog_post_code_edit.setObjectName("dialogPostCodeEdit")
        self.dialog_country_text_label = QLabel("country:")
        self.dialog_country_text_label.setObjectName("dialogCountryTextLabel")
        self.dialog_country_edit = QLineEdit()
        self.dialog_country_edit.setObjectName("dialogCountryEdit")
        buttons_layout = QHBoxLayout()
        self.dialog_add_contact_pushbutton = QPushButton("add")
        self.dialog_add_contact_pushbutton.setObjectName("dialogAddContactPushbutton")
        self.dialog_add_contact_pushbutton.setFixedSize(70, 40)
        self.dialog_cancel_pushbutton = QPushButton("cancel")
        self.dialog_cancel_pushbutton.setObjectName("dialogCancelPushbutton")
        self.dialog_cancel_pushbutton.setFixedSize(70, 40)
        fields = [
            (self.dialog_first_name_text_label, self.dialog_first_name_edit),
            (self.dialog_second_name_text_label, self.dialog_second_name_edit),
            (self.dialog_relationship_text_label, self.dialog_relationship_combobox),
            (self.dialog_email_text_label, self.dialog_email_edit),
            (self.dialog_phone_number_text_label, self.dialog_phone_number_edit),
            (self.dialog_address_text_label, self.dialog_address_edit),
            (self.dialog_city_text_label, self.dialog_city_edit),
            (self.dialog_post_code_text_label, self.dialog_post_code_edit),
            (self.dialog_country_text_label, self.dialog_country_edit),
        ]
        for label, edit in fields:
            form_layout.addRow(label, edit)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.dialog_add_contact_pushbutton)
        buttons_layout.addWidget(self.dialog_cancel_pushbutton)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        return main_layout