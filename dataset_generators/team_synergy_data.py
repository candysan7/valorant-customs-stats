from .DatasetGenerator import DatasetGenerator
from util import filter_players
from Match import Match
from constants.misc import *
from constants.players import *


class TeamSynergyDataGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "team-synergy-data.json"
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
