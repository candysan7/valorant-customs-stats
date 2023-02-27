from datetime import datetime, time, timedelta

from pytz import timezone

from constants.misc import *
from constants.players import *
from Match import Match
from util import filter_players

from .DatasetGenerator import DatasetGenerator


class RecentLobbyWinRatesGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "recent-lobby-win-rates.json"
        self.out_json = {
            player_name: {
                WINRATE: None,
                WINS: 0,
                GAMES: 0,
            }
            for player_name in PLAYER_NAMES
        }

        self.curr_date = datetime.combine(
            datetime(year=2022, month=10, day=9),
            time.max,
            tzinfo=timezone("US/Pacific"),
        )
        self.start_date = self.curr_date - timedelta(days=90)

    def accumulate(self, match: Match):
        if match.time > self.start_date:
            for player_name in filter_players(match.all_players):
                player_entry = self.out_json[player_name]

                # Update winrate
                if match.player_did_win(player_name):
                    player_entry[WINS] += 1
                if match.player_did_play(player_name):
                    player_entry[GAMES] += 1

    def finalize(self, minified=False):
        for player_name in PLAYER_NAMES:
            player_entry = self.out_json[player_name]

            if player_entry[GAMES] != 0:
                player_entry[WINRATE] = round(
                    100 * player_entry[WINS] / player_entry[GAMES]
                )

        return self.out_json
