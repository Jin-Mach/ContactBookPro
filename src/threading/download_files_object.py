import requests

from PyQt6.QtCore import QObject, pyqtSignal

from src.utilities.application_support_provider import ApplicationSupportProvider
from src.utilities.files_provider import FilesProvider
from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class DownloadFilesObject(QObject):
    download_finished = pyqtSignal(bool)
    download_progress = pyqtSignal(int, int)
    def __init__(self, files_provider: FilesProvider, application_support_provider: ApplicationSupportProvider) -> None:
        super().__init__()
        self.setObjectName("downloadFilesObject")
        self.files_provider = files_provider
        self.application_support_provider = application_support_provider
        self.connection_name = f"downloadFilesThread{id(self)}"


    def download_files(self) -> None:
        try:
            missing_files = self.get_missing_files()
            if not missing_files:
                self.download_finished.emit(True)
                return
            if not self.application_support_provider.connection_result():
                self.download_finished.emit(False)
                return
            total_value = len(missing_files)
            download_value = 0
            for key, value in missing_files.items():
                directory = value.parent
                directory.mkdir(parents=True, exist_ok=True)
                response = requests.get(key, timeout=10)
                if 200 <= response.status_code < 300 and response.content:
                    if value.exists():
                        value.unlink()
                    with open(str(value), "wb") as file:
                        file.write(response.content)
                        download_value += 1
                        self.download_progress.emit(download_value, total_value)
                else:
                    self.download_finished.emit(False)
                    return
            self.download_finished.emit(True)
            return
        except requests.exceptions.RequestException as e:
            ErrorHandler.write_log_exception(self.__class__.__name__, e)
            self.download_finished.emit(False)
            return
        except Exception as e:
            ErrorHandler.write_log_exception(self.__class__.__name__, e)
            self.download_finished.emit(False)
            return

    def get_missing_files(self) -> dict:
        missing_files_list = [
            self.files_provider.check_json_files(),
            self.files_provider.check_icon_files(),
            self.files_provider.check_font_files(),
            self.files_provider.check_manual_files(),
            self.files_provider.check_about_files()
        ]
        download_files = {}
        for files in missing_files_list:
            if files is None:
                return {}
            download_files.update(files)
        return download_files