from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit


class WorkWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogWorkWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_work_email_text_label = QLabel("email:")
        self.dialog_work_email_text_label.setObjectName("dialogWorkEmailTextLabel")
        self.dialog_work_email_edit = QLineEdit()
        self.dialog_work_email_edit.setObjectName("dialogWorkEmailEdit")
        self.dialog_work_phone_number_text_label = QLabel("phone:")
        self.dialog_work_phone_number_text_label.setObjectName("dialogWorkPhoneNumberTextLabel")
        self.dialog_work_phone_number_edit = QLineEdit()
        self.dialog_work_phone_number_edit.setObjectName("dialogPhoneNumberEdit")
        self.dialog_work_address_text_label = QLabel("address:")
        self.dialog_work_address_text_label.setObjectName("dialogWorkAddressTextLabel")
        self.dialog_work_address_edit = QLineEdit()
        self.dialog_work_address_edit.setObjectName("dialogWorkAddressEdit")
        self.dialog_work_city_text_label = QLabel("city:")
        self.dialog_work_city_text_label.setObjectName("dialogWorkCityTextLabel")
        self.dialog_work_city_edit = QLineEdit()
        self.dialog_work_city_edit.setObjectName("dialogWorkCityEdit")
        self.dialog_work_post_code_text_label = QLabel("post code:")
        self.dialog_work_post_code_text_label.setObjectName("dialogPostCodeTextLabel")
        self.dialog_work_post_code_edit = QLineEdit()
        self.dialog_work_post_code_edit.setObjectName("dialogPostCodeEdit")
        self.dialog_work_country_text_label = QLabel("country:")
        self.dialog_work_country_text_label.setObjectName("dialogWorkCountryTextLabel")
        self.dialog_work_country_edit = QLineEdit()
        self.dialog_work_country_edit.setObjectName("dialogWorkCountryEdit")
        widgets = [
            (self.dialog_work_email_text_label, self.dialog_work_email_edit),
            (self.dialog_work_phone_number_text_label, self.dialog_work_phone_number_edit),
            (self.dialog_work_address_text_label, self.dialog_work_address_edit),
            (self.dialog_work_city_text_label, self.dialog_work_city_edit),
            (self.dialog_work_post_code_text_label, self.dialog_work_post_code_edit),
            (self.dialog_work_country_text_label, self.dialog_work_country_edit),
        ]
        for label, edit in widgets:
            main_layout.addRow(label, edit)
        return main_layout
