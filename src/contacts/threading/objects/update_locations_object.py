from geopy.geocoders import Nominatim

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.contacts_utilities.query_provider import QueryProvider
from src.utilities.check_connection import connection_result
from src.utilities.logger_provider import get_logger

# noinspection PyUnresolvedReferences
class UpdateLocationsObject(QObject):
    finished = pyqtSignal(list)

    def __init__(self, db_path: str, main_window: QMainWindow) -> None:
        super().__init__()
        self.setObjectName("updateLocationsObject")
        self.db_path = db_path
        self.main_window = main_window
        self.connection_name = f"updateLocationsThread{id(self)}"
        QTimer.singleShot(5 * 60 * 1000, self.get_locations)

    def get_locations(self) -> None:
        db_connection = None
        updated_contacts = []
        try:
            if not connection_result():
                self.finished.emit(updated_contacts)
                return
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(updated_contacts)
                return
            location_contacts = QueryProvider.create_update_locations_query(db_connection, self.main_window)
            if location_contacts is None:
                self.finished.emit(updated_contacts)
                return
            geolocator = Nominatim(user_agent="contact_book_pro", timeout=2)
            for contact in location_contacts:
                contact_id = contact[0]
                street = contact[1]
                house_number = contact[2]
                city = contact[3]
                post_code = contact[4]
                country = contact[5]
                full_address = f"{house_number}, {city}, {post_code}, {country}"
                if street:
                    full_address = f"{street}, {house_number}, {city}, {post_code}, {country}"
                location = geolocator.geocode(full_address)
                if location:
                    updated_contacts.append((contact_id, (location.latitude, location.longitude)))
            self.finished.emit(updated_contacts)
        except Exception as e:
            logger = get_logger()
            logger.error(f"{self.objectName()}: {e}", exc_info=True)
            self.finished.emit(updated_contacts)
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)