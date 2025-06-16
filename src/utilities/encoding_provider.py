import sys

def get_encoding() -> str:
    encoding = "utf-8"
    if sys.platform.startswith("win"):
        encoding = "cp1250"
    return encoding