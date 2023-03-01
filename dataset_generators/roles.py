from constants import *
from Match import Match
from util import filter_players

from .DatasetGenerator import DatasetGenerator


class RolesGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "roles.json"
        self.out_json = {role_name: 0 for role_name in ROLE_NAMES}

    def accumulate(self, match: Match):
        for player_name in filter_players(match.all_players):
            player_stats = match.all_players[player_name]
            self.out_json[AGENT_NAME_TO_ROLE[player_stats.agent]] += 1

    def finalize(self, minified=False):
        return self.out_json
