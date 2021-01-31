"""Entrypoint for pulling season schedules, game stats and generating training data."""
import argparse
from scrape.season import get_seasons
from scrape.game import get_game_stats
import json


def parse_season_arg(season):
    """Check whether user has input multiple seasons. Remove whitespace."""
    season_split = season.split(",")
    if len(season_split) > 1:
        return [s.strip() for s in season_split]
    else:
        return [season.strip()]


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-season",
        metavar="-s",
        help="Season to pull stats for. Ex. 2020 Ex. 2020,2019,2018",
        required=True,
    )

    args = parser.parse_args()
    seasons = parse_season_arg(args.season)
    print(f"Pulling for seasons: {seasons}")
    season_game_map = get_seasons(seasons)
    print(f"Obtained schedules for seasons: {seasons}")
    game_results = []
    for season in seasons:
        print(f"Pulling game stats for season {season}.")
        game_results.append(get_game_stats(season_game_map, season))
        print(f"Done pulling game stats for season {season}.")

    stats_data_path = f"{','.join(seasons)}_game_results.json"
    with open(stats_data_path, "w") as outfile:
        print(f"Writing data to {stats_data_path}")
        json.dump(game_results, outfile)
