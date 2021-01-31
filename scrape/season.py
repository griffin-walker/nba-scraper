"""Get and parse season schedule."""

from bs4 import BeautifulSoup, element
from tqdm import tqdm

from scrape.query import get_and_soup


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
        except AttributeError:
            None
    return parsed_rows


def get_season_schedule(season: int):
    season_months = get_season_months(season=season)
    games = []
    for season_month in tqdm(season_months):
        month_soup = get_and_soup(extension=season_month["extension"])
        month_games = parse_monthly_schedule(month_soup)
        games.extend(month_games)
    return games


def get_seasons(seasons: list):
    season_game_map = {}
    for season in tqdm(seasons):
        games = get_season_schedule(season=season)
        season_game_map[season] = games
    return season_game_map
