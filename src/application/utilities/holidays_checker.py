import datetime
import pathlib
import holidays

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def get_local_holidays() -> list[datetime.date | str] | None:
    try:
        languages_path = pathlib.Path(__file__).parents[3].joinpath("languages")
        languages_folder = []
        for folder in languages_path.iterdir():
            if folder.is_dir():
                languages_folder.append(str(folder.name))
        if not languages_folder:
            return None
        language = str(LanguageProvider.language_code)
        if not language in languages_folder:
            return None
        current_date = datetime.date.today()
        local_holidays = holidays.country_holidays(country=language.split("_")[1], years=[current_date.year])
        current_holidays = local_holidays.get(datetime.date(2025, 1, 1))
        if not current_holidays:
            return None
        return [current_date, current_holidays]
    except Exception as e:
        ErrorHandler.exception_handler(e)
        return None