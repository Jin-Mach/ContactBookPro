class CheckUpdateProvider:

    @staticmethod
    def check_update(widget_name: str, default_data: list, new_data: list) -> tuple:
        slicing_data = CheckUpdateProvider.slice_new_data(default_data, new_data)
        default_data, new_data = slicing_data
        if widget_name == "dialogMandatoryWidget":
            default_address = default_data[6:11]
            new_address = new_data[6:11]
            if default_data != new_data:
                    if default_address != new_address:
                        return True, False
                    return False, False
            return True, True
        else:
            return default_data == new_data,

    @staticmethod
    def slice_new_data(default_data: list, new_data: list) -> tuple[list, list]:
        len_default = len(default_data)
        sliced_new_data = new_data[:len_default]
        return default_data, sliced_new_data

    @staticmethod
    def check_data_changed(new_data: list) -> bool:
        checked_data = []
        for data in new_data[:-1]:
            data_changed = data[-1][-1]
            checked_data.append(data_changed)
        return all(checked_data)