from PyQt6.QtCore import QDate, QLocale


def format_date(iso_date: str) -> str:
    if not iso_date:
        return ""
    date = QDate.fromString(iso_date.strip(), "yyyy-MM-dd")
    if not date.isValid():
        return ""
    locale = QLocale()
    return locale.toString(date, locale.FormatType.ShortFormat)