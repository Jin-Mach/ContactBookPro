from functools import partial

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout, QPushButton

from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class SearchDeatilsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("searchDetaisWidget")
        self.operator_width = 150
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.search_photo_text_label = QLabel()
        self.search_photo_text_label.setObjectName("searchPhotoTextLabel")
        self.search_photo_combobox = QComboBox()
        self.search_photo_combobox.setObjectName("searchPhotoCombobox")
        self.search_photo_combobox.setFixedWidth(200)
        self.search_title_text_label = QLabel()
        self.search_title_text_label.setObjectName("searchTitleTextLabel")
        self.search_title_edit = QLineEdit()
        self.search_title_edit.setObjectName("searchTitleEdit")
        self.search_title_operator = QComboBox()
        self.search_title_operator.setObjectName("searchTitleOperator")
        self.search_title_operator.setFixedWidth(self.operator_width)
        self.search_birthday_text_label = QLabel()
        self.search_birthday_text_label.setObjectName("searchBirthdayTextLabel")
        self.search_birthday_edit = QLineEdit()
        self.search_birthday_edit.setObjectName("searchBirthdayEdit")
        self.search_birthday_operator = QComboBox()
        self.search_birthday_operator.setObjectName("searchBirthdayOperator")
        self.search_birthday_operator.setFixedWidth(self.operator_width)
        self.search_notes_text_label = QLabel()
        self.search_notes_text_label.setObjectName("searchNotesTextLabel")
        self.search_notes_edit = QLineEdit()
        self.search_notes_edit.setObjectName("searcNotesEdit")
        self.search_notes_operator = QComboBox()
        self.search_notes_operator.setObjectName("searchNotesOperator")
        self.search_notes_operator.setFixedWidth(self.operator_width)
        fields = [
            (self.search_photo_text_label, self.search_photo_combobox, None),
            (self.search_title_text_label, self.search_title_edit, self.search_title_operator),
            (self.search_birthday_text_label, self.search_birthday_edit, self.search_birthday_operator),
            (self.search_notes_text_label, self.search_notes_edit, self.search_notes_operator)
        ]
        tooltip_text = LanguageProvider.get_tooltips_text("advancedSearchDialog")
        for label, edit, operator in fields:
            layout = QHBoxLayout()
            clear_filter_pushbutton = QPushButton()
            clear_filter_pushbutton.setObjectName("clearFilterPushbutton")
            IconProvider.set_buttons_icon("advancedSearchDialog", [clear_filter_pushbutton], QSize(25, 25))
            if clear_filter_pushbutton.objectName() in tooltip_text:
                clear_filter_pushbutton.setToolTip(tooltip_text[clear_filter_pushbutton.objectName()])
                clear_filter_pushbutton.setToolTipDuration(5000)
            clear_filter_pushbutton.clicked.connect(partial(SearchDeatilsWidget.reset_row_filter, edit, operator))
            layout.addWidget(edit)
            if isinstance(edit, QComboBox):
                layout.addStretch()
            if isinstance(edit, QLineEdit):
                layout.addWidget(operator)
            layout.addWidget(clear_filter_pushbutton)
            main_layout.addRow(label, layout)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            widgets = self.findChildren((QLabel, QComboBox, QLineEdit))
            for widget in widgets:
                if isinstance(widget, QLabel):
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text[widget.objectName()])
                elif isinstance(widget, QComboBox):
                    if widget.objectName().endswith("Combobox") and widget.objectName() in ui_text:
                        widget.addItems(ui_text[widget.objectName()])
                    else:
                        widget.addItems(ui_text["operators"])
                elif isinstance(widget, QLineEdit):
                    if widget.objectName() in ui_text:
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def reset_row_filter(edit: QWidget,  operator: QComboBox) -> None:
        if isinstance(edit, QComboBox):
            edit.setCurrentIndex(0)
        else:
            edit.clear()
            operator.setCurrentIndex(0)

    def reset_all_filters(self) -> None:
        widgets = self.findChildren((QComboBox, QLineEdit))
        for widget in widgets:
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            else:
                widget.clear()