from config import PLAYER_NAMES
from constants import *
from Match import Match
from util import filter_players

from .DatasetGenerator import DatasetGenerator

HEADSHOTS = "headshots"
HEADSHOT_RATE = "headshot_rate"
BODYSHOTS = "bodyshots"
BODYSHOT_RATE = "bodyshot_rate"
LEGSHOTS = "legshots"
LEGSHOT_RATE = "legshot_rate"
BULLETS = "bullets"
KNIFE_KILLS = "knife_kills"
KNIFE_DEATHS = "knife_deaths"
TEAM_DAMAGE = "team_damage"
SELF_DAMAGE = "self_damage"
BOMB_DEATHS = "bomb_deaths"
AVERAGE_TIME_ALIVE_ON_WON_ATTACK_ROUNDS = "average_time_alive_on_won_attack_rounds"
AVERAGE_TIME_ALIVE_ON_LOST_ATTACK_ROUNDS = "average_time_alive_on_lost_attack_rounds"


class WallOfShameGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "wall-of-shame.json"
        self.out_json = {
            player_name: {
                HEADSHOTS: 0,
                HEADSHOT_RATE: None,
                BODYSHOTS: 0,
                BODYSHOT_RATE: None,
                LEGSHOTS: 0,
                LEGSHOT_RATE: None,
                BULLETS: 0,
                KNIFE_KILLS: 0,
                KNIFE_DEATHS: 0,
                TEAM_DAMAGE: 0,
                SELF_DAMAGE: 0,
                PLANTS: 0,
                BOMB_DEATHS: 0,
                AVERAGE_TIME_ALIVE_ON_WON_ATTACK_ROUNDS: 0,
                AVERAGE_TIME_ALIVE_ON_LOST_ATTACK_ROUNDS: 0,
            }
            for player_name in PLAYER_NAMES
        }
        self.won_attack_rounds = {player_name: 0 for player_name in PLAYER_NAMES}
        self.lost_attack_rounds = {player_name: 0 for player_name in PLAYER_NAMES}

    def accumulate(self, match: Match):
        for player_name in filter_players(match.all_players):
            self.out_json[player_name][PLANTS] += match.all_players[player_name].plants

        for _round in match.rounds:
            for damage_event in _round.damage_events:
                giver_name = damage_event.giver_name
                receiver_name = damage_event.receiver_name

                if giver_name in PLAYER_NAMES:
                    if (
                        match.players_in_same_team(giver_name, receiver_name)
                        and damage_event.damage < 800
                    ):
                        if giver_name == receiver_name:
                            self.out_json[giver_name][
                                SELF_DAMAGE
                            ] += damage_event.damage
                        else:
                            self.out_json[giver_name][
                                TEAM_DAMAGE
                            ] += damage_event.damage
                    else:
                        self.out_json[giver_name][HEADSHOTS] += damage_event.headshots
                        self.out_json[giver_name][BODYSHOTS] += damage_event.bodyshots
                        self.out_json[giver_name][LEGSHOTS] += damage_event.legshots

                    self.out_json[giver_name][BULLETS] += (
                        damage_event.headshots
                        + damage_event.bodyshots
                        + damage_event.legshots
                    )

            # If a player is resurrected, we only want to add their time alive once
            handled_players = set()
            for kill in _round.kills:
                killer_name = kill.killer_name
                victim_name = kill.victim_name

                if (
                    victim_name not in handled_players
                    and _round.player_stats[victim_name].side == ATTACKERS
                    and victim_name in PLAYER_NAMES
                ):
                    handled_players.add(victim_name)
                    if _round.winning_side == ATTACKERS:
                        self.out_json[victim_name][
                            AVERAGE_TIME_ALIVE_ON_WON_ATTACK_ROUNDS
                        ] += kill.round_time
                    else:
                        self.out_json[victim_name][
                            AVERAGE_TIME_ALIVE_ON_LOST_ATTACK_ROUNDS
                        ] += kill.round_time

                if kill.weapon_name == "Melee":
                    if killer_name in PLAYER_NAMES:
                        self.out_json[killer_name][KNIFE_KILLS] += 1
                    if victim_name in PLAYER_NAMES:
                        self.out_json[victim_name][KNIFE_DEATHS] += 1

                if kill.weapon_name == "Bomb":
                    if victim_name in PLAYER_NAMES:
                        self.out_json[victim_name][BOMB_DEATHS] += 1

            for player_name in filter_players(match.all_players):
                if (
                    _round.player_stats[player_name].side != ATTACKERS
                    or _round.win_method == SURRENDERED
                ):
                    continue

                if _round.winning_side == ATTACKERS:
                    self.won_attack_rounds[player_name] += 1
                else:
                    self.lost_attack_rounds[player_name] += 1

                # If a player didn't die, they survived the whole round
                if _round.player_stats[player_name].deaths == 0:
                    if _round.winning_side == ATTACKERS:
                        self.out_json[player_name][
                            AVERAGE_TIME_ALIVE_ON_WON_ATTACK_ROUNDS
                        ] += _round.duration
                    else:
                        self.out_json[player_name][
                            AVERAGE_TIME_ALIVE_ON_LOST_ATTACK_ROUNDS
                        ] += _round.duration

    def finalize(self, minified=False):
        for player_name in PLAYER_NAMES:
            self.out_json[player_name][HEADSHOT_RATE] = round(
                100
                * self.out_json[player_name][HEADSHOTS]
                / self.out_json[player_name][BULLETS]
            )
            self.out_json[player_name][BODYSHOT_RATE] = round(
                100
                * self.out_json[player_name][BODYSHOTS]
                / self.out_json[player_name][BULLETS]
            )
            self.out_json[player_name][LEGSHOT_RATE] = round(
                100
                * self.out_json[player_name][LEGSHOTS]
                / self.out_json[player_name][BULLETS]
            )
            self.out_json[player_name][AVERAGE_TIME_ALIVE_ON_WON_ATTACK_ROUNDS] = round(
                self.out_json[player_name][AVERAGE_TIME_ALIVE_ON_WON_ATTACK_ROUNDS]
                / (self.won_attack_rounds[player_name] * 1000)
            )
            self.out_json[player_name][
                AVERAGE_TIME_ALIVE_ON_LOST_ATTACK_ROUNDS
            ] = round(
                self.out_json[player_name][AVERAGE_TIME_ALIVE_ON_LOST_ATTACK_ROUNDS]
                / (self.lost_attack_rounds[player_name] * 1000)
            )

            if minified:
                del self.out_json[player_name][HEADSHOTS]
                del self.out_json[player_name][HEADSHOT_RATE]
                del self.out_json[player_name][BODYSHOTS]
                del self.out_json[player_name][LEGSHOTS]

        return self.out_json
