from config import PLAYER_NAMES
from constants import *
from Match import Match
from util import filter_players, is_player_of_interest

from .DatasetGenerator import DatasetGenerator

ASSISTANT_NAME = "assistant_name"


class AssistsReceivedPerStandardGameGenerator(DatasetGenerator):
    def __init__(self):
        super().__init__("assists-received-per-standard-game")
        self.out_json = {
            player_name: {
                assistant_name: {
                    ASSISTANT_NAME: assistant_name,
                    ASSISTS_PER_STANDARD_GAME: None,
                    ASSISTS: 0,
                    ROUNDS: 0,
                }
                for assistant_name in PLAYER_NAMES
            }
            for player_name in PLAYER_NAMES
        }

    def accumulate(self, match: Match):
        for player_name in filter_players(match.all_players):
            for assistant_name in filter_players(match.all_players):
                if match.players_in_same_team(player_name, assistant_name):
                    if player_name == assistant_name:
                        continue
                    self.out_json[player_name][assistant_name][ROUNDS] += len(
                        match.rounds
                    )
        for _round in match.rounds:
            # This will overwrite the round() function otherwise
            for kill in _round.kills:
                if kill.killer_name == kill.victim_name:
                    continue
                player_name = kill.killer_name
                if not is_player_of_interest(player_name):
                    continue
                for assistant_name in filter_players(kill.assistants):
                    self.out_json[player_name][assistant_name][ASSISTS] += 1

    def finalize(self, minified=False):
        for player_name in PLAYER_NAMES:
            for assistant_name in PLAYER_NAMES:
                if self.out_json[player_name][assistant_name][ROUNDS] != 0:
                    self.out_json[player_name][assistant_name][
                        ASSISTS_PER_STANDARD_GAME
                    ] = (
                        round(
                            10
                            * 25
                            * self.out_json[player_name][assistant_name][ASSISTS]
                            / self.out_json[player_name][assistant_name][ROUNDS]
                        )
                        / 10
                    )

        for player_name in self.out_json:
            self.out_json[player_name] = sorted(
                self.out_json[player_name].values(), key=lambda x: x[ASSISTANT_NAME]
            )

        return self.out_json
