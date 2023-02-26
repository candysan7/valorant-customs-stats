from .DatasetGenerator import DatasetGenerator
from util import filter_players
from Match import Match
from constants.misc import *
from constants.players import *


class EasiestMatchupsGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "easiest-matchups.json"
        self.out_json = {
            player_name: {
                opponent_name: {
                    OPPONENT_NAME: opponent_name,
                    WINRATE: None,
                    WINS: 0,
                    GAMES: 0,
                }
                for opponent_name in PLAYER_NAMES
            }
            for player_name in PLAYER_NAMES
        }

    def accumulate(self, match: Match):
        for player_name in filter_players(match.winning_players):
            for opponent_name in filter_players(match.losing_players):
                self.out_json[player_name][opponent_name][WINS] += 1
                self.out_json[player_name][opponent_name][GAMES] += 1
        for player_name in filter_players(match.losing_players):
            for opponent_name in filter_players(match.winning_players):
                self.out_json[player_name][opponent_name][GAMES] += 1

    def finalize(self, minified=False):
        for player_name in self.out_json:
            for opponent_name in self.out_json[player_name]:
                if self.out_json[player_name][opponent_name][GAMES] != 0:
                    self.out_json[player_name][opponent_name][WINRATE] = round(
                        100
                        * self.out_json[player_name][opponent_name][WINS]
                        / self.out_json[player_name][opponent_name][GAMES]
                    )

        for player_name in self.out_json:
            if minified:
                for opponent_name in PLAYER_NAMES:
                    del self.out_json[player_name][opponent_name][WINS]
                    del self.out_json[player_name][opponent_name][GAMES]
            self.out_json[player_name] = sorted(
                self.out_json[player_name].values(), key=lambda x: x[OPPONENT_NAME]
            )

        return self.out_json
