import json
from typing import Any
import pathlib

from src.utilities.language_provider import LanguageProvider


class MapKeys:
    default_path = pathlib.Path(__file__).parents[3].joinpath("languages")
    language_code = LanguageProvider.get_language_code()

    @staticmethod
    def mapping_keys(column_name: str, value: Any) -> str:
        try:
            file_path = MapKeys.default_path.joinpath(MapKeys.language_code, "export_settings.json")
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
        from src.utilities.logger_provider import get_logger
        logger = get_logger()
        logger.error(exception)