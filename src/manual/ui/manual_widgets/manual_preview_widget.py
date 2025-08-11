from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts

if TYPE_CHECKING:
    from src.manual.ui.manual_widgets.manual_treewidget import ManualTreeWidget


# noinspection PyUnresolvedReferences
class ManualPreviewWidget(QWidget):
    def __init__(self, tree_widget: "ManualTreeWidget", top_item_index: int, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualPreviewWidget")
        self.tree_widget = tree_widget
        self.top_item_index = top_item_index
        self.setLayout(self.create_gui())
        tab_widgets = [self.pdf_text_edit, self.qr_code_text_edit]
        apply_tab_texts(self.objectName(), self.manual_preview_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_preview_tab_widget = QTabWidget()
        self.manual_preview_tab_widget.currentChanged.connect(self.set_tree_item)
        self.pdf_text_edit = QTextEdit()
        self.pdf_text_edit.setObjectName("pdfPreviewTextEdit")
        self.pdf_text_edit.setReadOnly(True)
        self.pdf_text_edit.setText("pdf")
        self.qr_code_text_edit = QTextEdit()
        self.qr_code_text_edit.setObjectName("qrCodePreviewTextEdit")
        self.qr_code_text_edit.setReadOnly(True)
        self.qr_code_text_edit.setText("qr code")
        self.manual_preview_tab_widget.addTab(self.pdf_text_edit, "")
        self.manual_preview_tab_widget.addTab(self.qr_code_text_edit, "")
        main_layout.addWidget(self.manual_preview_tab_widget)
        return main_layout

    def set_tree_item(self) -> None:
        if not self.tree_widget.initialized:
            return
        top_item = self.tree_widget.topLevelItem(self.top_item_index)
        if top_item is None:
            return
        current_item = self.tree_widget.currentItem()
        if current_item is top_item:
            return
        tab_index = self.manual_preview_tab_widget.currentIndex()
        if tab_index is not None and 0 <= tab_index < top_item.childCount():
            item_to_select = top_item.child(tab_index)
        else:
            item_to_select = top_item
        self.tree_widget.setCurrentItem(item_to_select)
        parent = item_to_select.parent()
        while parent is not None:
            parent.setExpanded(True)
            parent = parent.parent()

    def set_current_tab(self, index: int) -> None:
        self.manual_preview_tab_widget.setCurrentIndex(index)