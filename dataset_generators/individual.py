from constants.misc import *
from constants.players import *
from constants.valorant import *
from Match import Match
from util import filter_players

from .DatasetGenerator import DatasetGenerator


class IndividualGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "individual.json"
        self.out_json = {
            player_name: PLAYER_INFO[player_name].copy()
            | {
                WINRATE: None,
                WINS: 0,
                GAMES: 0,
                MAPS: {
                    map_name: {ACS: None, SCORE: 0, ROUNDS: 0} for map_name in MAP_NAMES
                },
                AGENTS: {
                    agent_name: {
                        ROLE: AGENT_NAME_TO_ROLE[agent_name],
                        WINRATE: None,
                        WINS: 0,
                        GAMES: 0,
                    }
                    for agent_name in AGENT_NAMES
                },
                ROLES: {
                    role_name: {WINRATE: None, WINS: 0, GAMES: 0}
                    for role_name in ROLE_NAMES
                },
                TOP_AGENTS: [],
                TOP_ROLES: [],
            }
            for player_name in PLAYER_NAMES
        }

    def accumulate(self, match: Match):
        for player_name in filter_players(match.all_players):
            player_stats = match.all_players[player_name]
            player_entry = self.out_json[player_name]

            # Update winrate
            if match.player_did_win(player_name):
                player_entry[WINS] += 1
                player_entry[AGENTS][player_stats.agent][WINS] += 1
                player_entry[ROLES][AGENT_NAME_TO_ROLE[player_stats.agent]][WINS] += 1
            if match.player_did_play(player_name):
                player_entry[GAMES] += 1
                player_entry[MAPS][match.map][
                    SCORE
                ] += player_stats.average_combat_score * len(match.rounds)
                player_entry[MAPS][match.map][ROUNDS] += len(match.rounds)
                player_entry[AGENTS][player_stats.agent][GAMES] += 1
                player_entry[ROLES][AGENT_NAME_TO_ROLE[player_stats.agent]][GAMES] += 1

    def finalize(self, minified=False):
        for player_name in PLAYER_NAMES:
            player_entry = self.out_json[player_name]

            if player_entry[GAMES] != 0:
                player_entry[WINRATE] = round(
                    100 * player_entry[WINS] / player_entry[GAMES]
                )

            for map_name in MAP_NAMES:
                if player_entry[MAPS][map_name][ROUNDS] != 0:
                    player_entry[MAPS][map_name][ACS] = round(
                        player_entry[MAPS][map_name][SCORE]
                        / player_entry[MAPS][map_name][ROUNDS]
                    )

            for agent_name in AGENT_NAMES:
                if player_entry[AGENTS][agent_name][GAMES] != 0:
                    player_entry[AGENTS][agent_name][WINRATE] = round(
                        100
                        * player_entry[AGENTS][agent_name][WINS]
                        / player_entry[AGENTS][agent_name][GAMES]
                    )

            for role_name in ROLE_NAMES:
                if player_entry[ROLES][role_name][GAMES] != 0:
                    player_entry[ROLES][role_name][WINRATE] = round(
                        100
                        * player_entry[ROLES][role_name][WINS]
                        / player_entry[ROLES][role_name][GAMES]
                    )

        for player_name in PLAYER_NAMES:
            player_entry = self.out_json[player_name]

            for role_name in ROLE_NAMES:
                if player_entry[ROLES][role_name][GAMES] / player_entry[GAMES] > 0.3:
                    self.out_json[player_name][TOP_ROLES].append(role_name)

            agents_sorted_by_plays = sorted(
                self.out_json[player_name][AGENTS],
                key=lambda agent_name: (
                    -self.out_json[player_name][AGENTS][agent_name][GAMES],
                    agent_name,
                ),
            )
            self.out_json[player_name][TOP_AGENTS] = [
                agent_name for agent_name in agents_sorted_by_plays[:3]
            ]

            if minified:
                del self.out_json[player_name][WINS]
                for map_name in MAP_NAMES:
                    del self.out_json[player_name][MAPS][map_name][SCORE]
                    del self.out_json[player_name][MAPS][map_name][ROUNDS]
                for agent_name in AGENT_NAMES:
                    del self.out_json[player_name][AGENTS][agent_name][WINRATE]
                    del self.out_json[player_name][AGENTS][agent_name][WINS]

        return self.out_json
