from setuptools import setup, find_packages

def read_me() -> str:
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

setup(
    name="ContactBookPro",
    version="1.0",
    author="Jin-Mach",
    author_email="Ji82Ma@seznam.cz",
    description="A simple contact management app with location-based support and statistics, built with PyQt6.",
    long_description=read_me(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jin-Mach/ContactBookPro",
    packages=find_packages(),
    install_requires=[
        "folium>=0.20",
        "geopy>=2.4",
        "matplotlib>=3.10",
        "email-validator>=2.0",
        "phonenumbers>=9.0",
        "Pillow>=11.3",
        "python-dateutil>=2.9",
        "pytz>=2025.2",
        "PyQt6>=6.9",
        "PyQt6-WebEngine>=6.9",
        "PyYAML>=6.0",
        "qrcode>=8.2",
        "qt-material>=2.17",
        "reportlab>=4.4",
        "requests>=2.32",
        "tldextract>=5.3",
        "validators>=0.35",
        "vobject>=0.9.9",
        "xlsxwriter>=3.2",
        "pywin32; sys_platform=='win32'"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "contact_book=contact_book:create_app",
            ],
        },
    keywords="contact_book, pyqt6",
)