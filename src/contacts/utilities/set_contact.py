from typing import TYPE_CHECKING

from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.database.models.mandatory_model import MandatoryModel

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget


def show_selected_contact(mandatory_model: MandatoryModel, table_view: "ContactsTableviewWidget", status_bar: ContactsStatusbarWidget,
                          selected_id: int) -> None:
    mandatory_model.set_filter_by_id([selected_id])
    table_view.set_selected_contact()
    status_bar.set_count_text(mandatory_model.rowCount(), 0)