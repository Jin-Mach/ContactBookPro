import pathlib
import json
from json import JSONDecodeError


class FiltersProvider:
    filters_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("data", "user_filters.json")

    @staticmethod
    def add_new_filter(filter_name: str, new_filter: dict) -> tuple[bool, str]:
        try:
            filters = FiltersProvider.get_filters_data()
            if not filter_name in filters.keys():
                filters[filter_name] = new_filter
                with open(str(FiltersProvider.filters_path), "w", encoding="utf-8") as file:
                    json.dump(filters, file, indent=2)
                return True, "success"
            return False, "exists"
        except Exception as e:
            FiltersProvider.write_log_exception(e)
            return False, "error"

    @staticmethod
    def remove_filter() -> None:
        pass

    @staticmethod
    def get_filters_data() -> dict[str, dict]:
        try:
            with open(str(FiltersProvider.filters_path), "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        from src.utilities.logger_provider import get_logger
        logger = get_logger()
        logger.error(exception, exc_info=True)