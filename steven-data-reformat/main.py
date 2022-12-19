import json, os.path
from datetime import datetime, timedelta

from Match import Match
from util import aggregate_matches, filter_players
from constants import *

output_dir = "./steven-data-reformat/out/"

matches: list[Match] = []
with open("./steven-data-reformat/data.json", mode="r") as f:
    data = json.load(f)
    matches = sorted([Match(match_json) for match_json in data], key=lambda m: m.time)
    f.close()

if __name__ == "__main__":
    with open(os.path.join(output_dir, "individual.json"), mode="w") as f:
        out_json = {
            player_name: {WINRATE: None, WINS: 0, GAMES: 0}
            for player_name in player_names
        }
        for match in matches:
            for player_name in player_names:
                player_entry = out_json[player_name]
                if match.player_did_win(player_name):
                    player_entry[WINS] += 1
                if match.player_did_play(player_name):
                    player_entry[GAMES] += 1
                if player_entry[GAMES] != 0:
                    player_entry[WINRATE] = round(
                        100 * player_entry[WINS] / player_entry[GAMES]
                    )
        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "teammate-synergy.json"), mode="w") as f:
        out_json = {
            player_name: {
                teammate_name: {WINRATE: None, WINS: 0, GAMES: 0}
                for teammate_name in player_names
            }
            for player_name in player_names
        }

        for match in matches:
            for player_name in filter_players(match.winning_players):
                for teammate_name in filter_players(match.winning_players):
                    out_json[player_name][teammate_name][WINS] += 1
                    out_json[player_name][teammate_name][GAMES] += 1
            for player_name in filter_players(match.losing_players):
                for teammate_name in filter_players(match.losing_players):
                    out_json[player_name][teammate_name][GAMES] += 1
        for player_name in out_json:
            for teammate_name in out_json[player_name]:
                if out_json[player_name][teammate_name][GAMES] != 0:
                    out_json[player_name][teammate_name][WINRATE] = round(
                        100
                        * out_json[player_name][teammate_name][WINS]
                        / out_json[player_name][teammate_name][GAMES]
                    )

        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "easiest-matchups.json"), mode="w") as f:
        out_json = {
            player_name: {
                opponent_name: {WINRATE: None, WINS: 0, GAMES: 0}
                for opponent_name in player_names
            }
            for player_name in player_names
        }

        for match in matches:
            for player_name in filter_players(match.winning_players):
                for opponent_name in filter_players(match.losing_players):
                    out_json[player_name][opponent_name][WINS] += 1
                    out_json[player_name][opponent_name][GAMES] += 1
            for player_name in filter_players(match.losing_players):
                for opponent_name in filter_players(match.winning_players):
                    out_json[player_name][opponent_name][GAMES] += 1
        for player_name in out_json:
            for opponent_name in out_json[player_name]:
                if out_json[player_name][opponent_name][GAMES] != 0:
                    out_json[player_name][opponent_name][WINRATE] = round(
                        100
                        * out_json[player_name][opponent_name][WINS]
                        / out_json[player_name][opponent_name][GAMES]
                    )

        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "maps.json"), mode="w") as f:
        out_json = {map: 0 for map in maps}
        for match in matches:
            out_json[match.map] += 1
        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "winrate-over-time.json"), mode="w") as f:

        def winrate(matches: list[Match], previous_block):
            block_data = {
                player_name: {WINRATE: None, WINS: 0, GAMES: 0}
                for player_name in player_names
            }
            for match in matches:
                for winner_name in filter_players(match.winning_players):
                    block_data[winner_name][WINS] += 1
                for player_name in filter_players(match.all_players):
                    block_data[player_name][GAMES] += 1
            for player_name, player_stats in block_data.items():
                if player_stats[GAMES] != 0:
                    player_stats[WINRATE] = round(
                        100 * player_stats[WINS] / player_stats[GAMES]
                    )
            return block_data

        out_json = aggregate_matches(matches, winrate)
        json.dump(out_json, f, indent=2, default=str)
        f.close()

    with open(
        os.path.join(output_dir, "cumulative-winrate-over-time.json"), mode="w"
    ) as f:

        def cumulative_winrate(matches: list[Match], previous_block):
            if previous_block is not None:
                block_data = {
                    player_name: previous_block["data"][player_name].copy()
                    for player_name in player_names
                }
            else:
                block_data = {
                    player_name: {WINRATE: None, WINS: 0, GAMES: 0}
                    for player_name in player_names
                }
            for match in matches:
                for winner_name in filter_players(match.winning_players):
                    block_data[winner_name][WINS] += 1
                for player_name in filter_players(match.all_players):
                    block_data[player_name][GAMES] += 1
            for player_name, player_stats in block_data.items():
                if player_stats[GAMES] != 0:
                    player_stats[WINRATE] = round(
                        100 * player_stats[WINS] / player_stats[GAMES]
                    )
            return block_data

        out_json = aggregate_matches(matches, cumulative_winrate)
        json.dump(out_json, f, indent=2, default=str)
        f.close()
