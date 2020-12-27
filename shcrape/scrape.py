"""Module for scraping basketball reference for game stats."""

import requests
from bs4 import BeautifulSoup, element
import json
from tqdm import tqdm


BASE_URL = "https://basketball-reference.com"
HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}


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


def get_season_months(season: int) -> list:
    season_ext = f"/leagues/NBA_{season}_games.html"
    season_soup = get_and_soup(extension=season_ext)
    season_months = season_soup.find("div", {"class": "filter"}).find_all("a")
    month_extensions = [
        {"month": a.contents[0], "extension": a.get("href")} for a in season_months
    ]
    return month_extensions


def parse_schedule_row(row: element.Tag) -> dict:
    reference_ext = (
        row.find("td", {"data-stat": "box_score_text"}).find("a").get("href")
    )
    home_team = row.find("td", {"data-stat": "home_team_name"}).find("a").contents[0]
    away_team = row.find("td", {"data-stat": "visitor_team_name"}).find("a").contents[0]
    visitor_id = (
        row.find("td", {"data-stat": "visitor_team_name"}).get("csk").split(".")[0]
    )
    home_pts = row.find("td", {"data-stat": "home_pts"}).contents[0]
    away_pts = row.find("td", {"data-stat": "visitor_pts"}).contents[0]
    row_dict = {
        "reference_extension": reference_ext,
        "home": home_team,
        "away": away_team,
        "home_pts": home_pts,
        "away_pts": away_pts,
        "away_id": visitor_id,
    }
    return row_dict


def parse_monthly_schedule(month_soup: BeautifulSoup):
    trs = month_soup.find_all("tr")
    parsed_rows = []
    for tr in trs:
        try:
            if tr.find("th", {"data-stat": "date_game"}).contents == ["Date"]:
                continue
            else:
                parsed_rows.append(parse_schedule_row(tr))
        except ValueError:
            raise Exception("Value Error")
    return parsed_rows


def get_season_schedule(season: int):
    season_months = get_season_months(season=season)
    games = []
    for season_month in tqdm(season_months):
        month_soup = get_and_soup(extension=season_month["extension"])
        month_games = parse_monthly_schedule(month_soup)
        games.extend(month_games)
    return games


def get_seasons(seasons=range(2011, 2022)):
    season_game_map = {}
    for season in tqdm(seasons):
        games = get_season_schedule(season=season)
        season_game_map[season] = games
    return season_game_map


if __name__ == "__main__":
    season_game_map = get_seasons()
    with open("season_game_map.json", "w") as outfile:
        json.dump(season_game_map, outfile)
