from config import PLAYER_NAMES
from constants import *
from Match import Match
from util import filter_players

from .DatasetGenerator import DatasetGenerator

SCORE_DELTA = "score_delta"
DID_NOT_PLAY = 0
RED_TEAM = 1
BLUE_TEAM = -1


class TeamSynergyDataGenerator(DatasetGenerator):
    def __init__(self):
        super().__init__("team-synergy-data")
        self.out_json = []

    def accumulate(self, match: Match):
        out_row = (
            {player_name: DID_NOT_PLAY for player_name in PLAYER_NAMES}
            | {player_name + "_acs": DID_NOT_PLAY for player_name in PLAYER_NAMES}
            | {SCORE_DELTA: 0}
        )

        for player_name in filter_players(match.team_red):
            out_row[player_name] = RED_TEAM
        for player_name in filter_players(match.team_blue):
            out_row[player_name] = BLUE_TEAM
        for player_name in filter_players(match.all_players):
            out_row[player_name + "_acs"] = match.all_players[
                player_name
            ].average_combat_score
        out_row[SCORE_DELTA] = match.score_red - match.score_blue

        self.out_json.append(out_row)

    def finalize(self, minified=False):
        return self.out_json
