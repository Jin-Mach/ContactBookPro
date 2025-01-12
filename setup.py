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
        "PyQt6>=6.7.1",
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