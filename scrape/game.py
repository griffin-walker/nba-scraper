"""Get and parse game stats."""

from tqdm import tqdm
from bs4 import BeautifulSoup, Comment

from scrape.query import get_and_soup


def parse_game_factors(game_soup):
    # parse comment within four factors html
    all_four_factors_comment = game_soup.find(
        "div", {"id": "all_four_factors"}
    ).find_all(string=lambda text: isinstance(text, Comment))
    assert len(all_four_factors_comment) == 1

    # convert comment obj to soup
    all_four_factors_soup = BeautifulSoup(all_four_factors_comment[0], "html.parser")
    four_factor_stats = all_four_factors_soup.find("tbody").find_all("tr")

    # loop over table cols to get four factor stats
    four_factor_stat_map = {}
    for stat_line in four_factor_stats:
        team_id = stat_line.find("th", {"data-stat": "team_id"}).find("a").contents[0]
        stats = ["pace", "efg_pct", "tov_pct", "orb_pct", "ft_rate", "off_rtg"]
        stat_map = {}
        for stat in stats:
            stat_map.update(
                {stat: float(stat_line.find("td", {"data-stat": stat}).contents[0])}
            )
        four_factor_stat_map.update({team_id: stat_map})

    return four_factor_stat_map


def parse_game_stats(game_meta, game_soup):
    stat_tables = get_stat_tables(game_meta, game_soup)
    four_factors = parse_game_factors(game_soup)
    # update with 4 factors stats
    stat_tables[game_meta["home_id"]]["advanced"].update(
        four_factors[game_meta["home_id"]]
    )
    stat_tables[game_meta["away_id"]]["advanced"].update(
        four_factors[game_meta["away_id"]]
    )
    return stat_tables


def parse_stat_table(table):
    table_elements = table.find("tfoot").find_all("td", {"class": "right"})
    stat_map = {}
    for stat in table_elements:
        try:
            stat_map.update({stat.get("data-stat"): stat.contents[0]})
        except IndexError:
            continue
    return stat_map


def get_stat_tables(game_meta, game_soup):
    home_id = game_meta["home_id"]
    away_id = game_meta["away_id"]
    basic_home_stats = game_soup.find("div", {"id": f"all_box-{home_id}-game-basic"})
    advanced_home_stats = game_soup.find(
        "div", {"id": f"all_box-{home_id}-game-advanced"}
    )
    basic_away_stats = game_soup.find("div", {"id": f"all_box-{away_id}-game-basic"})
    advanced_away_stats = game_soup.find(
        "div", {"id": f"all_box-{away_id}-game-advanced"}
    )
    return {
        home_id: {
            "advanced": parse_stat_table(advanced_home_stats),
            "basic": parse_stat_table(basic_home_stats),
        },
        away_id: {
            "advanced": parse_stat_table(advanced_away_stats),
            "basic": parse_stat_table(basic_away_stats),
        },
    }


def get_game_stats(season_game_map, season):
    game_results = []
    for game in tqdm(season_game_map[season][0:10]):
        game_soup = get_and_soup(game["reference_extension"])
        game_meta = game.copy()
        game_meta.update(
            {"home_id": game_meta["reference_extension"].split(".html")[0][-3:]}
        )
        game_stats = parse_game_stats(game_meta, game_soup)
        game_stats.update({"meta": game_meta})
        game_results.append(game_stats)
    return game_results
