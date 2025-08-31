import json
import pathlib

from typing import Any

from src.utilities.error_handler import ErrorHandler


class FiltersProvider:
    filters_path = pathlib.Path(__file__).parents[3].joinpath("data", "user_filters.json")
    filters_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def add_new_filter(filter_name: str, new_filter: dict) -> tuple[bool, str]:
        try:
            filters = FiltersProvider.get_filters_data()
            if not filter_name in filters.keys():
                filters[filter_name] = new_filter
                with open(FiltersProvider.filters_path, "w", encoding="utf-8") as file:
                    json.dump(filters, file, indent=2)
                return True, "success"
            return False, "exists"
        except Exception as e:
            ErrorHandler.write_log_exception(FiltersProvider.__class__.__name__, e)
            return False, "error"

    @staticmethod
    def remove_filter(filter_name: str) -> None:
        try:
            saved_filters = FiltersProvider.get_filters_data()
            if filter_name in saved_filters:
                saved_filters.pop(filter_name, None)
                with open(FiltersProvider.filters_path, "w", encoding="utf-8") as file:
                    json.dump(saved_filters, file, indent=2)
        except Exception as e:
            ErrorHandler.write_log_exception(FiltersProvider.__class__.__name__, e)

    @staticmethod
    def get_filters_data() -> dict[str, dict]:
        try:
            with open(FiltersProvider.filters_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def return_selected_filter(filter_name: str) -> dict[str, list[Any]]:
        try:
            with open(FiltersProvider.filters_path, "r", encoding="utf-8") as file:
                filters = json.load(file)
                if filter_name in filters:
                    return filters[filter_name]
                return {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def delete_filters_file() -> None:
        try:
            if FiltersProvider.filters_path.exists() and FiltersProvider.filters_path.is_file():
                FiltersProvider.filters_path.unlink()
        except Exception as e:
            ErrorHandler.write_log_exception(FiltersProvider.__class__.__name__, e)