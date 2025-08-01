from PyQt6.QtCore import QThreadPool

from src.contacts.threading.location_thread import LocationThread
from src.utilities.application_support_provider import ApplicationSupportProvider


def update_models_data(index: int, contact_id: int, models: list, data: list, now: str, signal_provider, map_controller) -> bool:
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
        if data[0][-1] == (True, False) and ApplicationSupportProvider.connection_result():
            QThreadPool.globalInstance().start(LocationThread(contact_id, data[0][0], signal_provider))
        models[4].select()
    return data_changed