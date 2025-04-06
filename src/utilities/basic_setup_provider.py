import pathlib
import requests


class BasicSetupProvider:
    default_path = pathlib.Path(__file__).parent.parent
    missing_urls = []

    @staticmethod
    def check_json_files() -> dict:
        required_files = ["dialog_text.json", "errors_text.json", "headers_text.json", "ui_text.json"]
        json_files_path = BasicSetupProvider.default_path.joinpath("languages")
        json_url = "https://raw.githubusercontent.com/Jin-Mach/ContactBookPro/main/src/languages"
        missing_json_urls = {}
        try:
            if json_files_path.exists() and json_files_path.is_dir():
                for language_dir in json_files_path.iterdir():
                    if language_dir.is_dir():
                        json_files = language_dir.glob("*.json")
                        json_list = []
                        for file in json_files:
                            file_name = pathlib.Path(file).name
                            json_list.append(file_name)
                        for file in required_files:
                            if file not in json_list:
                                file_url = f"{json_url}/{language_dir.name}/{file}"
                                missing_json_urls[file_url] = language_dir.joinpath(file)
            return missing_json_urls
        except Exception as e:
            BasicSetupProvider.write_log_exception(e)
            return {}

    @staticmethod
    def check_icon_files() -> dict:
        required_files = [
            "qt_calendar_nextmonth_icon.png", "qt_calendar_prevmonth_icon.png", "addNewContactPushbutton_icon.png",
            "deleteAllContactsPushbutton_icon.png", "deleteContactPushbutton_icon.png", "searchPushbutton_icon.png",
            "updateContactPushbutton_icon.png", "dog_image.png", "mainWindowDatabaseButton_icon.png", "window_icon.png",
            "no_user_photo.png", "facebookPushbutton_icon.png", "githubPushbutton_icon.png",
            "instagramPushbutton_icon.png",
            "linkedinPushbutton_icon.png", "websitePushbutton_icon.png", "xPushbutton_icon.png"
        ]
        icon_files_path = BasicSetupProvider.default_path.joinpath("icons")
        icons_url_base = "https://github.com/Jin-Mach/ContactBookPro/raw/main/src/icons"
        missing_icons_urls = {}
        found_icons = set()
        icon_folders = {
            "qt_calendar_nextmonth_icon.png": "calendarWidget",
            "qt_calendar_prevmonth_icon.png": "calendarWidget",
            "addNewContactPushbutton_icon.png": "contactsToolbarWidget",
            "deleteAllContactsPushbutton_icon.png": "contactsToolbarWidget",
            "deleteContactPushbutton_icon.png": "contactsToolbarWidget",
            "searchPushbutton_icon.png": "contactsToolbarWidget",
            "updateContactPushbutton_icon.png": "contactsToolbarWidget",
            "dog_image.png": "mainWindow",
            "mainWindowDatabaseButton_icon.png": "mainWindow",
            "window_icon.png": "mainWindow",
            "no_user_photo.png": "personalDetailWidget",
            "facebookPushbutton_icon.png": "tabInfoWidget",
            "githubPushbutton_icon.png": "tabInfoWidget",
            "instagramPushbutton_icon.png": "tabInfoWidget",
            "linkedinPushbutton_icon.png": "tabInfoWidget",
            "websitePushbutton_icon.png": "tabInfoWidget",
            "xPushbutton_icon.png": "tabInfoWidget"
        }
        try:
            if icon_files_path.exists() and icon_files_path.is_dir():
                for icon_dir in icon_files_path.iterdir():
                    if icon_dir.is_dir():
                        for icon_file in icon_dir.glob("*.png"):
                            found_icons.add(icon_file.name)
            for icon in required_files:
                if icon not in found_icons:
                    if icon in icon_folders:
                        folder = icon_folders[icon]
                        missing_icons_urls[f"{icons_url_base}/{folder}/{icon}"] = icon_files_path.joinpath(folder, icon)
            return missing_icons_urls
        except Exception as e:
            BasicSetupProvider.write_log_exception(e)
            return {}

    @staticmethod
    def check_qss_files() -> dict:
        qss_file_path = BasicSetupProvider.default_path.joinpath("styles", "light_blue_style.qss")
        try:
            if not qss_file_path.exists():
                return {"https://raw.githubusercontent.com/Jin-Mach/ContactBookPro/main/src/styles/light_blue_style.qss": qss_file_path}
            return {}
        except Exception as e:
            BasicSetupProvider.write_log_exception(e)
            return {}

    @staticmethod
    def download_files() -> bool:
        missing_files = [BasicSetupProvider.check_json_files(), BasicSetupProvider.check_icon_files(), BasicSetupProvider.check_qss_files()]
        download_files = {}
        for files in missing_files:
            if files:
                download_files.update(files)
        if not download_files:
            return True
        try:
            for key, value in download_files.items():
                directory = value.parent
                directory.mkdir(parents=True, exist_ok=True)
                response = requests.get(key)
                if 200 <= response.status_code < 300 and response.content:
                    if value.exists():
                        value.unlink()
                    with open(str(value), "wb") as file:
                        file.write(response.content)
                else:
                    return False
        except requests.exceptions.RequestException as e:
            BasicSetupProvider.write_log_exception(e)
            return False
        return True

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        from src.utilities.logger_provider import get_logger
        logger  = get_logger()
        logger.error(exception, exc_info=True)