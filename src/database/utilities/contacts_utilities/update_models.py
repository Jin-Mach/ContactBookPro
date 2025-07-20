from PyQt6.QtCore import QThreadPool

from src.contacts.threading.location_thread import LocationThread
from src.contacts.threading.signal_provider import SignalProvider
from src.map.controllers.map_controller import MapController


def update_models_data(index: int, contact_id: int, models: list, data: list, now: str, signal_provider: SignalProvider,
                       map_controller: MapController) -> bool:
    data_changed = False
    model_map = {
        models[0]: data[0],
        models[1]: data[1],
        models[2]: data[2],
        models[3]: data[3]
    }
    for model, (value, flags) in model_map.items():
        if model.objectName() == "mandatoryModel":
            if flags != (True, True):
                model.update_contact(index, value)
                data_changed = True
        else:
            if flags == (False,):
                model.update_contact(contact_id, value)
                data_changed = True
    if data_changed:
        for model, (value, flags) in model_map.items():
            if flags != (True, True):
                model.select()
        models[4].update_contact(contact_id, now)
        if data[0][-1] == (True, False):
            def on_location_updated(id_contact, coords):
                models[4].update_location_data(id_contact, coords)
                map_controller.create_map()
            QThreadPool.globalInstance().start(LocationThread(contact_id, data[0][0], signal_provider))
            signal_provider.contact_coordinates.connect(on_location_updated)
        models[4].select()
    return data_changed