from src.utilities.logger_provider import get_logger

from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim

from PyQt6.QtCore import QRunnable

from src.contacts.threading.signal_provider import SignalProvider


class LocationThread(QRunnable):
    def __init__(self, contact_id: int, contact_address: list, signal: SignalProvider) -> None:
        super().__init__()
        self.contact_id = contact_id
        self.contact_street = contact_address[6]
        self.contact_house_number = contact_address[7]
        self.contact_city = contact_address[8]
        self.contact_post_code = contact_address[9]
        self.contact_country = contact_address[10]
        self.signal = signal

    def run(self) -> None:
        try:
            full_address = f"{self.contact_house_number}, {self.contact_city}, {self.contact_post_code}, {self.contact_country}"
            if self.contact_street:
                full_address = f"{self.contact_street}, {self.contact_house_number}, {self.contact_city}, {self.contact_post_code}, {self.contact_country}"
            geolocator = Nominatim(user_agent="contact_book_pro", timeout=2)
            location = geolocator.geocode(full_address)
            if location:
                self.signal.contact_coordinates.emit(self.contact_id, (location.latitude, location.longitude))
            else:
                self.signal.contact_coordinates.emit(self.contact_id, (None, None))
        except (GeocoderTimedOut, GeocoderUnavailable, Exception) as e:
            logger = get_logger()
            logger.error(e)
            self.signal.contact_coordinates.emit(self.contact_id, (None, None))