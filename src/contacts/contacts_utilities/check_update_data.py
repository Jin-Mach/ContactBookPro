def check_update(widget_name: str, default_data: list, new_data: list) -> tuple:
    if widget_name == "dialogMandatoryWidget":
        default_address = [default_data[6], default_data[7], default_data[8], default_data[9], default_data[10]]
        new_address = [new_data[6], new_data[7], new_data[8], new_data[9], new_data[10]]
        if default_data != new_data:
            if default_address != new_address:
                return True, False
            return False, False
        return True, True
    else:
        return default_data == new_data,