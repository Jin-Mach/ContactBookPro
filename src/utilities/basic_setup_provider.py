import pathlib
import requests

from src.utilities.logger_provider import get_logger


class BasicSetupProvider:
    default_path = pathlib.Path(__file__).parents[2]
    default_path.mkdir(parents=True, exist_ok=True)
    missing_urls = []

    @staticmethod
    def check_json_files() -> dict:
        required_files = ["dialog_text.json", "errors_text.json", "export_settings.json", "headers_text.json",
                          "language_info.json", "menu_text.json", "search_dialog_text.json", "statustips_text.json",
                          "tooltips_text.json", "ui_text.json", "user_filters_dialog_text.json"]
        json_files_path = BasicSetupProvider.default_path.joinpath("languages")
        json_url = "https://raw.githubusercontent.com/Jin-Mach/ContactBookPro/main/languages"
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
            "clearFilterPushbutton_icon.png", "currentFilterButton_icon.png", "addNewContactPushbutton_icon.png",
            "advancedSearchPushbutton_icon.png", "deleteAllContactsPushbutton_icon.png",
            "deleteContactPushbutton_icon.png",
            "resetFilterPushbutton_icon.png", "searchPushbutton_icon.png", "updateContactPushbutton_icon.png",
            "userFiltersPushbutton_icon.png", "addContactAction_icon.png", "contactCheckBirthdayAction_icon.png",
            "contactCheckDuplicityAction_icon.png", "copyEmailAction_icon.png", "copyNameAction_icon.png",
            "copyPhoneNumberAction_icon.png", "deleteContactAction_icon.png", "exportAllDataCsvAction_icon.png",
            "exportAllDataExcelAction_icon.png", "exportCsvMenu_icon.png", "exportExcelMenuAction_icon.png",
            "exportFilteredDataCsvAction_icon.png", "exportFilteredDataExcelAction_icon.png",
            "exportVcardAction_icon.png", "previewAllContactsListAction_icon.png"
            "previewContactAction_icon.png", "previewContactListAction_icon.png", "previewFilteredContactsListAction_icon.png",
            "previewQrCodeAction_icon.png",
            "updateContactAction_icon.png", "dialogCalendarPushbutton_icon.png", "dialogGetPhotoPushbutton_icon.png",
            "dialogResetCalendarPushbutton_icon.png", "dialogResetPhotoButton_icon.png", "no_user_photo.png",
            "deleteFilterButton_icon.png", "mainWindowLogo.png", "mainWindowMapButton_icon.png", "mainWindowDatabaseButton_icon.png", "mainWindowStatisticsButton_icon.png",
            "pdfFitPageButton_icon.png", "pdfSaveAsButton_icon.png", "pdfZoomInButton_icon.png",
            "pdfZoomOutButton_icon.png",
            "female_icon.png", "male_icon.png", "facebookPushbutton_icon.png", "githubPushbutton_icon.png",
            "instagramPushbutton_icon.png", "linkedinPushbutton_icon.png", "websitePushbutton_icon.png",
            "xPushbutton_icon.png",
            "deleteFilterPushbutton_icon.png"
        ]
        icon_folders = {
            "clearFilterPushbutton_icon.png": "advancedSearchDialog",
            "currentFilterButton_icon.png": "advancedSearchDialog",
            "addNewContactPushbutton_icon.png": "contactsToolbarWidget",
            "advancedSearchPushbutton_icon.png": "contactsToolbarWidget",
            "deleteAllContactsPushbutton_icon.png": "contactsToolbarWidget",
            "deleteContactPushbutton_icon.png": "contactsToolbarWidget",
            "resetFilterPushbutton_icon.png": "contactsToolbarWidget",
            "searchPushbutton_icon.png": "contactsToolbarWidget",
            "updateContactPushbutton_icon.png": "contactsToolbarWidget",
            "userFiltersPushbutton_icon.png": "contactsToolbarWidget",
            "addContactAction_icon.png": "contextMenu",
            "contactCheckBirthdayAction_icon.png": "contextMenu",
            "contactCheckDuplicityAction_icon.png": "contextMenu",
            "copyEmailAction_icon.png": "contextMenu",
            "copyNameAction_icon.png": "contextMenu",
            "copyPhoneNumberAction_icon.png": "contextMenu",
            "deleteContactAction_icon.png": "contextMenu",
            "exportAllDataCsvAction_icon.png": "contextMenu",
            "exportAllDataExcelAction_icon.png": "contextMenu",
            "exportCsvMenu_icon.png": "contextMenu",
            "exportExcelMenuAction_icon.png": "contextMenu",
            "exportFilteredDataCsvAction_icon.png": "contextMenu",
            "exportFilteredDataExcelAction_icon.png": "contextMenu",
            "exportVcardAction_icon.png": "contextMenu",
            "previewAllContactsListAction_icon.png": "contextMenu",
            "previewContactAction_icon.png": "contextMenu",
            "previewContactListAction_icon.png": "contextMenu",
            "previewFilteredContactsListAction_icon.png": "contextMenu",
            "previewQrCodeAction_icon.png": "contextMenu",
            "updateContactAction_icon.png": "contextMenu",
            "dialogCalendarPushbutton_icon.png": "dialogPersonalDetailWidget",
            "dialogGetPhotoPushbutton_icon.png": "dialogPersonalDetailWidget",
            "dialogResetCalendarPushbutton_icon.png": "dialogPersonalDetailWidget",
            "dialogResetPhotoButton_icon.png": "dialogPersonalDetailWidget",
            "no_user_photo.png": "dialogPersonalDetailWidget",
            "deleteFilterButton_icon.png": "filtersTableviewWidget",
            "mainWindowLogo.png": "mainWindow",
            "mainWindowMapButton_icon.png": "mainWindow",
            "mainWindowDatabaseButton_icon.png": "mainWindow",
            "mainWindowStatisticsButton_icon.png": "mainWindow",
            "pdfFitPageButton_icon.png": "pdfPreviewDialog",
            "pdfSaveAsButton_icon.png": "pdfPreviewDialog",
            "pdfZoomInButton_icon.png": "pdfPreviewDialog",
            "pdfZoomOutButton_icon.png": "pdfPreviewDialog",
            "female_icon.png": "personalTabInfoWidget",
            "male_icon.png": "personalTabInfoWidget",
            "facebookPushbutton_icon.png": "tabInfoWidget",
            "githubPushbutton_icon.png": "tabInfoWidget",
            "instagramPushbutton_icon.png": "tabInfoWidget",
            "linkedinPushbutton_icon.png": "tabInfoWidget",
            "websitePushbutton_icon.png": "tabInfoWidget",
            "xPushbutton_icon.png": "tabInfoWidget",
            "deleteFilterPushbutton_icon.png": "userFiltersListWidget"
        }
        icon_files_path = BasicSetupProvider.default_path.joinpath("icons")
        icons_url_base = "https://raw.githubusercontent.com/Jin-Mach/ContactBookPro/main/icons"
        missing_icons_urls = {}
        found_icons = set()

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
                        url = f"{icons_url_base}/{folder}/{icon}"
                        local_path = icon_files_path.joinpath(folder, icon)
                        missing_icons_urls[url] = local_path
            return missing_icons_urls
        except Exception as e:
            BasicSetupProvider.write_log_exception(e)
            return {}

    @staticmethod
    def check_font_files() -> dict:
        required_fonts = ["TimesNewRoman.ttf"]
        fonts_directory = BasicSetupProvider.default_path.joinpath("fonts")
        fonts_base_url = "https://github.com/Jin-Mach/ContactBookPro/raw/main/fonts"
        missing_fonts_urls = {}
        found_fonts = set()
        try:
            if fonts_directory.exists() and fonts_directory.is_dir():
                for font_file in fonts_directory.glob("*.ttf"):
                    font_name = font_file.name
                    found_fonts.add(font_name)
            for font_name in required_fonts:
                if font_name not in found_fonts:
                    font_url = f"{fonts_base_url}/{font_name}"
                    font_target_path = fonts_directory.joinpath(font_name)
                    missing_fonts_urls[font_url] = font_target_path
            return missing_fonts_urls
        except Exception as e:
            BasicSetupProvider.write_log_exception(e)
            return {}

    @staticmethod
    def download_files() -> bool:
        missing_files = [BasicSetupProvider.check_json_files(), BasicSetupProvider.check_icon_files(),
                         BasicSetupProvider.check_font_files()]
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
        logger  = get_logger()
        logger.error(exception, exc_info=True)