import codecs
from setuptools import setup, find_packages
from stonktop import __version__

with codecs.open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="stonktop",
    description="A stock ticker tracker for the terminal",
    long_description=README,
    long_description_content_type="text/markdown",
    version=__version__,
    packages=find_packages(),
    author="Shawn Mittal",
    url="https://github.com/shawnmittal/stonktop",
    keywords=["stonks", "cash", "money"],
    author_email="shawn@shawnmittal.com,
    install_requires=["urwid", "yfinance"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["stonktop=stonktop.stonktop:cli",]},
)