from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget


def show_selected_contact(mandatory_model: "MandatoryModel", table_view: "ContactsTableviewWidget", status_bar: "ContactsStatusbarWidget",
                          selected_id: int) -> None:
    mandatory_model.set_filter_by_id([selected_id])
    table_view.select_contact_by_id(selected_id)
    status_bar.set_count_text(mandatory_model.rowCount(), mandatory_model.total_rows)