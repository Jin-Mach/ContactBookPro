from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QHBoxLayout, QStackedWidget

from src.manual.ui.manual_widgets.manual_check_widget import ManualCheckWidget
from src.manual.ui.manual_widgets.manual_contacts_widget import ManualContactsWidget
from src.manual.ui.manual_widgets.manual_export_widget import ManualExportWidget
from src.manual.ui.manual_widgets.manual_introduction_widget import ManualIntroductionWidget
from src.manual.ui.manual_widgets.manual_map_widget import ManualMapWidget
from src.manual.ui.manual_widgets.manual_preview_widget import ManualPreviewWidget
from src.manual.ui.manual_widgets.manual_statistics_widget import ManualStatisticsWidget
from src.manual.ui.manual_widgets.manual_treewidget import ManualTreeWidget


class ManualMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualMainWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        self.tree_widget = ManualTreeWidget(self)
        self.tree_widget.itemClicked.connect(self.set_stacked_widget)
        self.stacked_widget = QStackedWidget()
        self.manual_introduction_widget = ManualIntroductionWidget(self)
        self.manual_contacts_widget = ManualContactsWidget(self)
        self.manual_export_widget = ManualExportWidget(self)
        self.manual_preview_widget = ManualPreviewWidget(self)
        self.manual_chcek_widget = ManualCheckWidget(self)
        self.manual_map_widget = ManualMapWidget(self)
        self.manual_statistics_widget = ManualStatisticsWidget(self)
        self.stacked_widget.addWidget(self.manual_introduction_widget)
        self.stacked_widget.addWidget(self.manual_contacts_widget)
        self.stacked_widget.addWidget(self.manual_export_widget)
        self.stacked_widget.addWidget(self.manual_preview_widget)
        self.stacked_widget.addWidget(self.manual_chcek_widget)
        self.stacked_widget.addWidget(self.manual_map_widget)
        self.stacked_widget.addWidget(self.manual_statistics_widget)
        main_layout.addWidget(self.tree_widget, stretch=0)
        main_layout.addWidget(self.stacked_widget, stretch=1)
        return main_layout

    def set_manual_widget_to_default(self) -> None:
        self.tree_widget.hide_child_items()
        self.stacked_widget.setCurrentIndex(0)
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, "set_default_tab"):
            current_widget.set_default_tab(0)

    def set_stacked_widget(self) -> None:
        stacked_index, tab_index = self.tree_widget.currentItem().data(0, Qt.ItemDataRole.UserRole)
        self.stacked_widget.setCurrentIndex(stacked_index)
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, "set_current_tab"):
            current_widget.set_current_tab(tab_index)