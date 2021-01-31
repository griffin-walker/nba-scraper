"""HTML Getters."""
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://basketball-reference.com"
HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}


class InvalidQuery(Exception):
    """Raise if query fails."""

    pass


def get_and_soup(extension: str) -> BeautifulSoup:
    response = requests.get(BASE_URL + extension, headers=HEADERS)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        raise Exception
