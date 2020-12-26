""""""

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://basketball-reference.com"
path = "/boxscores/202012230CHI.html"
HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

SEASONS = list(range(2011, 2022))

# <div class="filter"> # grab a.s and their href


def iterate_season_months(month_refs: list):
    return


def parse_season_schedule(season_soup: BeautifulSoup):
    return


def get_schedule(season: str):
    """"""
    return


def get_and_soup(extension: str) -> BeautifulSoup:
    """
    :param game_id: Combination of date (YYYYMMDD) and home team identifer (ex. CHI)
    :type game_id: str

    :return: Parsed html page result
    :rtype: BeautifulSoup
    """
    response = requests.get(BASE_URL + extension, headers=HEADERS)
    if response.ok:
        soup = BeautifulSoup(response.content)
        return soup
    else:
        return response.status_code


if __name__ == "__main__":
    soup = get_and_soup(extension=path)
    print(soup)
