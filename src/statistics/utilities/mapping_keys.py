import json
import pathlib

from typing import Any

from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class MapKeys:
    default_path = pathlib.Path(__file__).parents[3].joinpath("languages")

    @staticmethod
    def mapping_keys(column_name: str, value: Any) -> str:
        try:
            language_code = LanguageProvider.get_language_code()
            file_path = MapKeys.default_path.joinpath(language_code, "export_settings.json")
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            map = data["exportDataProvider"][f"{column_name}Map"]
            if value in map:
                value = map.get(value, "")
            return str(value)
        except Exception as e:
            MapKeys.write_log_exception(e)
            return ""

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(f"{MapKeys.__class__.__name__}: {exception}", exc_info=True)