import json, os.path
from datetime import datetime, timedelta, time
from pytz import timezone

from Match import Match
from util import aggregate_matches, filter_players, is_player_of_interest
from constants.misc import *
from constants.players import *
from constants.valorant import *

output_dir = "./out"

matches: list[Match] = []
with open("./data.json", mode="r") as f:
    data = json.load(f)
    # data.json is sorted in process_scrape.py
    # matches = sorted([Match(match_json) for match_json in data], key=lambda m: m.time)
    f.close()

if __name__ == "__main__":
    with open(os.path.join(output_dir, "meta.json"), mode="w") as f:
        out_json = {
            "most_recent_url": matches[-1].url,
        }
        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "data-frame-friendly.json"), mode="w") as f:
        out_json = {i: match_json for i, match_json in enumerate(data)}
        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "wall-of-shame.json"), mode="w") as f:
        out_json = {
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
            }
            for player_name in PLAYER_NAMES
        }

        for match in matches:
            for player_name in filter_players(match.all_players):
                out_json[player_name][PLANTS] += match.all_players[player_name].plants

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
                                out_json[giver_name][SELF_DAMAGE] += damage_event.damage
                            else:
                                out_json[giver_name][TEAM_DAMAGE] += damage_event.damage
                        else:
                            out_json[giver_name][HEADSHOTS] += damage_event.headshots
                            out_json[giver_name][BODYSHOTS] += damage_event.bodyshots
                            out_json[giver_name][LEGSHOTS] += damage_event.legshots

                        out_json[giver_name][BULLETS] += (
                            damage_event.headshots
                            + damage_event.bodyshots
                            + damage_event.legshots
                        )

                for kill in _round.kills:
                    killer_name = kill.killer_name
                    victim_name = kill.victim_name

                    if kill.weapon_name == "Melee":
                        if killer_name in PLAYER_NAMES:
                            out_json[killer_name][KNIFE_KILLS] += 1
                        if victim_name in PLAYER_NAMES:
                            out_json[victim_name][KNIFE_DEATHS] += 1

                    if kill.weapon_name == "Bomb":
                        if victim_name in PLAYER_NAMES:
                            out_json[victim_name][BOMB_DEATHS] += 1

        for player_name in PLAYER_NAMES:
            out_json[player_name][HEADSHOT_RATE] = round(
                100 * out_json[player_name][HEADSHOTS] / out_json[player_name][BULLETS]
            )
            out_json[player_name][BODYSHOT_RATE] = round(
                100 * out_json[player_name][BODYSHOTS] / out_json[player_name][BULLETS]
            )
            out_json[player_name][LEGSHOT_RATE] = round(
                100 * out_json[player_name][LEGSHOTS] / out_json[player_name][BULLETS]
            )

        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "recent-lobby-win-rates.json"), mode="w") as f:
        out_json = {
            player_name: {
                WINRATE: None,
                WINS: 0,
                GAMES: 0,
            }
            for player_name in PLAYER_NAMES
        }

        curr_date = datetime.combine(
            datetime(year=2022, month=10, day=9),
            time.max,
            tzinfo=timezone("US/Pacific"),
        )
        start_date = curr_date - timedelta(days=90)

        for match in matches:
            if match.time > start_date:
                for player_name in filter_players(match.all_players):
                    player_stats = match.all_players[player_name]
                    player_entry = out_json[player_name]

                    # Update winrate
                    if match.player_did_win(player_name):
                        player_entry[WINS] += 1
                    if match.player_did_play(player_name):
                        player_entry[GAMES] += 1

        for player_name in PLAYER_NAMES:
            player_entry = out_json[player_name]

            if player_entry[GAMES] != 0:
                player_entry[WINRATE] = round(
                    100 * player_entry[WINS] / player_entry[GAMES]
                )

        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "individual.json"), mode="w") as f:
        out_json = {
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

        for match in matches:
            for player_name in filter_players(match.all_players):
                player_stats = match.all_players[player_name]
                player_entry = out_json[player_name]

                # Update winrate
                if match.player_did_win(player_name):
                    player_entry[WINS] += 1
                    player_entry[AGENTS][player_stats.agent][WINS] += 1
                    player_entry[ROLES][AGENT_NAME_TO_ROLE[player_stats.agent]][
                        WINS
                    ] += 1
                if match.player_did_play(player_name):
                    player_entry[GAMES] += 1
                    player_entry[MAPS][match.map][
                        SCORE
                    ] += player_stats.average_combat_score * len(match.rounds)
                    player_entry[MAPS][match.map][ROUNDS] += len(match.rounds)
                    player_entry[AGENTS][player_stats.agent][GAMES] += 1
                    player_entry[ROLES][AGENT_NAME_TO_ROLE[player_stats.agent]][
                        GAMES
                    ] += 1

        for player_name in PLAYER_NAMES:
            player_entry = out_json[player_name]

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
            player_entry = out_json[player_name]

            for role_name in ROLE_NAMES:
                if player_entry[ROLES][role_name][GAMES] / player_entry[GAMES] > 0.3:
                    out_json[player_name][TOP_ROLES].append(role_name)

            agents_sorted_by_plays = sorted(
                out_json[player_name][AGENTS],
                key=lambda agent_name: (
                    -out_json[player_name][AGENTS][agent_name][GAMES],
                    agent_name,
                ),
            )
            out_json[player_name][TOP_AGENTS] = [
                agent_name
                for agent_name in agents_sorted_by_plays[:3]
                # {
                #     AGENT: agent_name,
                #     FULL_BODY_IMAGE_URL: AGENT_NAME_TO_FULL_BODY_IMAGE_URL[agent_name],
                # }
                # for agent_name in agents_sorted_by_plays[:3]
            ]
        json.dump(out_json, f, indent=2)
        f.close()

    with open(
        os.path.join(output_dir, "assists-received-per-standard-game.json"), mode="w"
    ) as f:
        out_json = {
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

        for match in matches:
            for player_name in filter_players(match.all_players):
                for assistant_name in filter_players(match.all_players):
                    if match.players_in_same_team(player_name, assistant_name):
                        if player_name == assistant_name:
                            continue
                        out_json[player_name][assistant_name][ROUNDS] += len(
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
                        out_json[player_name][assistant_name][ASSISTS] += 1

        for player_name in PLAYER_NAMES:
            for assistant_name in PLAYER_NAMES:
                if out_json[player_name][assistant_name][ROUNDS] != 0:
                    out_json[player_name][assistant_name][ASSISTS_PER_STANDARD_GAME] = (
                        round(
                            10
                            * 25
                            * out_json[player_name][assistant_name][ASSISTS]
                            / out_json[player_name][assistant_name][ROUNDS]
                        )
                        / 10
                    )

        for player_name in out_json:
            out_json[player_name] = sorted(
                out_json[player_name].values(), key=lambda x: x[ASSISTANT_NAME]
            )

        json.dump(out_json, f, indent=2)
        f.close()

    with open(
        os.path.join(output_dir, "assists-given-per-standard-game.json"), mode="w"
    ) as f:
        out_json = {
            player_name: {
                assisted_name: {
                    ASSISTED_NAME: assisted_name,
                    ASSISTS_PER_STANDARD_GAME: None,
                    ASSISTS: 0,
                    ROUNDS: 0,
                }
                for assisted_name in PLAYER_NAMES
            }
            for player_name in PLAYER_NAMES
        }

        for match in matches:
            for player_name in filter_players(match.all_players):
                for assistant_name in filter_players(match.all_players):
                    if match.players_in_same_team(player_name, assistant_name):
                        if player_name == assistant_name:
                            continue
                        out_json[player_name][assistant_name][ROUNDS] += len(
                            match.rounds
                        )
            for _round in match.rounds:
                # This will overwrite the round() function otherwise
                for kill in _round.kills:
                    if kill.killer_name == kill.victim_name:
                        continue
                    assisted_name = kill.killer_name
                    if not is_player_of_interest(assisted_name):
                        continue
                    for player_name in filter_players(kill.assistants):
                        out_json[player_name][assisted_name][ASSISTS] += 1

        for player_name in PLAYER_NAMES:
            for assistant_name in PLAYER_NAMES:
                if out_json[player_name][assistant_name][ROUNDS] != 0:
                    out_json[player_name][assistant_name][ASSISTS_PER_STANDARD_GAME] = (
                        round(
                            10
                            * 25
                            * out_json[player_name][assistant_name][ASSISTS]
                            / out_json[player_name][assistant_name][ROUNDS]
                        )
                        / 10
                    )

        for player_name in out_json:
            out_json[player_name] = sorted(
                out_json[player_name].values(), key=lambda x: x[ASSISTED_NAME]
            )

        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "teammate-synergy.json"), mode="w") as f:
        out_json = {
            player_name: {
                teammate_name: {
                    TEAMMATE_NAME: teammate_name,
                    WINRATE: None,
                    WINS: 0,
                    GAMES: 0,
                }
                for teammate_name in PLAYER_NAMES
            }
            for player_name in PLAYER_NAMES
        }

        for match in matches:
            for player_name in filter_players(match.winning_players):
                for teammate_name in filter_players(match.winning_players):
                    if player_name == teammate_name:
                        continue
                    out_json[player_name][teammate_name][WINS] += 1
                    out_json[player_name][teammate_name][GAMES] += 1
            for player_name in filter_players(match.losing_players):
                for teammate_name in filter_players(match.losing_players):
                    if player_name == teammate_name:
                        continue
                    out_json[player_name][teammate_name][GAMES] += 1
        for player_name in out_json:
            for teammate_name in out_json[player_name]:
                if out_json[player_name][teammate_name][GAMES] != 0:
                    out_json[player_name][teammate_name][WINRATE] = round(
                        100
                        * out_json[player_name][teammate_name][WINS]
                        / out_json[player_name][teammate_name][GAMES]
                    )

        for player_name in out_json:
            out_json[player_name] = sorted(
                out_json[player_name].values(), key=lambda x: x[TEAMMATE_NAME]
            )
        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "easiest-matchups.json"), mode="w") as f:
        out_json = {
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

        for player_name in out_json:
            out_json[player_name] = sorted(
                out_json[player_name].values(), key=lambda x: x[OPPONENT_NAME]
            )
        json.dump(out_json, f, indent=2)
        f.close()

    with open(os.path.join(output_dir, "maps.json"), mode="w") as f:
        out_json = {map: 0 for map in MAP_NAMES}
        for match in matches:
            out_json[match.map] += 1
        json.dump(out_json, f, indent=2)
        f.close()

    with open(
        os.path.join(output_dir, "running-winrate-over-time.json"), mode="w"
    ) as f:

        out_json = []

        last_date = datetime.combine(
            datetime.today(), time.max, tzinfo=timezone("US/Pacific")
        )
        curr_date = datetime.combine(
            datetime(year=2022, month=10, day=9),
            time.max,
            tzinfo=timezone("US/Pacific"),
        )
        time_increment = timedelta(weeks=1)

        curr_block_start_date = curr_date - timedelta(days=90)

        i = 0
        j = 0
        while j <= len(matches):
            # Blocks look like (curr_block_start_date, curr_date]; should correspond to [i, j)
            while j < len(matches) and matches[j].time <= curr_date:
                j += 1
            while i < len(matches) and matches[i].time < curr_block_start_date:
                i += 1
            if i == len(matches) or curr_date > last_date:
                break

            block_data = {
                player_name: {WINRATE: None, WINS: 0, GAMES: 0}
                for player_name in PLAYER_NAMES
            }

            for match in matches[i:j]:
                for winner_name in filter_players(match.winning_players):
                    block_data[winner_name][WINS] += 1
                for player_name in filter_players(match.all_players):
                    block_data[player_name][GAMES] += 1
            for player_name, player_stats in block_data.items():
                if player_stats[GAMES] != 0:
                    player_stats[WINRATE] = round(
                        100 * player_stats[WINS] / player_stats[GAMES]
                    )

            out_json.append({"block_end_time": curr_date, "data": block_data})

            curr_date += time_increment
            curr_block_start_date += time_increment

        # Individually compute the present day
        i = len(matches)
        while i > 0 and matches[i - 1].time >= last_date - timedelta(days=90):
            i -= 1

        block_data = {
            player_name: {WINRATE: None, WINS: 0, GAMES: 0}
            for player_name in PLAYER_NAMES
        }

        for match in matches[i:]:
            for winner_name in filter_players(match.winning_players):
                block_data[winner_name][WINS] += 1
            for player_name in filter_players(match.all_players):
                block_data[player_name][GAMES] += 1
        for player_name, player_stats in block_data.items():
            if player_stats[GAMES] != 0:
                player_stats[WINRATE] = round(
                    100 * player_stats[WINS] / player_stats[GAMES]
                )

        out_json.append({"block_end_time": last_date, "data": block_data})

        json.dump(out_json, f, indent=2, default=str)
        f.close()

    with open(os.path.join(output_dir, "roles.json"), mode="w") as f:
        out_json = {role_name: 0 for role_name in ROLE_NAMES}

        for match in matches:
            for player_name in filter_players(match.all_players):
                player_stats = match.all_players[player_name]
                out_json[AGENT_NAME_TO_ROLE[player_stats.agent]] += 1

        json.dump(out_json, f, indent=2)
        f.close()

# Unused dataset functions

# with open(os.path.join(output_dir, "portion-of-stats.json"), mode="w") as f:
#     metrics = {
#         KILLS: lambda player_stats: player_stats.kills,
#         DEATHS: lambda player_stats: player_stats.deaths,
#         ASSISTS: lambda player_stats: player_stats.assists,
#         FIRST_KILLS: lambda player_stats: player_stats.first_kills,
#         FIRST_DEATHS: lambda player_stats: player_stats.first_deaths,
#     }

#     out_json = {
#         player_name: {
#             metric: {
#                 PERCENTAGE: None,
#                 COMMITTED: 0,
#                 WITNESSED: 0,
#             }
#             for metric in metrics
#         }
#         for player_name in PLAYER_NAMES
#     }

#     for match in matches:
#         for player_name in match.all_players:
#             player_stats = match.all_players[player_name]
#             for metric, fn in metrics.items():
#                 if player_name in PLAYER_NAMES:
#                     out_json[player_name][metric][COMMITTED] += fn(player_stats)
#             for player_name_to_update in filter_players(match.all_players):
#                 for metric, fn in metrics.items():
#                     out_json[player_name_to_update][metric][WITNESSED] += fn(
#                         player_stats
#                     )

#     for player_name in out_json:
#         for metric in metrics:
#             if out_json[player_name][metric][WITNESSED] == 0:
#                 continue
#             out_json[player_name][metric][PERCENTAGE] = round(
#                 100
#                 * out_json[player_name][metric][COMMITTED]
#                 / out_json[player_name][metric][WITNESSED]
#             )

#     json.dump(out_json, f, indent=2)
#     f.close()

# with open(os.path.join(output_dir, "winrate-over-time.json"), mode="w") as f:

#     def winrate(matches: list[Match], accumulator):
#         block_data = {
#             player_name: {WINRATE: None, WINS: 0, GAMES: 0}
#             for player_name in PLAYER_NAMES
#         }
#         for match in matches:
#             for winner_name in filter_players(match.winning_players):
#                 block_data[winner_name][WINS] += 1
#             for player_name in filter_players(match.all_players):
#                 block_data[player_name][GAMES] += 1
#         for player_name, player_stats in block_data.items():
#             if player_stats[GAMES] != 0:
#                 player_stats[WINRATE] = round(
#                     100 * player_stats[WINS] / player_stats[GAMES]
#                 )
#         return block_data

#     out_json = aggregate_matches(matches, winrate)
#     json.dump(out_json, f, indent=2, default=str)
#     f.close()

# with open(
#     os.path.join(output_dir, "cumulative-winrate-over-time.json"), mode="w"
# ) as f:

#     def cumulative_winrate(matches: list[Match], accumulator):
#         if len(accumulator) > 0:
#             block_data = {
#                 player_name: accumulator[-1]["data"][player_name].copy()
#                 for player_name in PLAYER_NAMES
#             }
#         else:
#             block_data = {
#                 player_name: {WINRATE: None, WINS: 0, GAMES: 0}
#                 for player_name in PLAYER_NAMES
#             }
#         for match in matches:
#             for winner_name in filter_players(match.winning_players):
#                 block_data[winner_name][WINS] += 1
#             for player_name in filter_players(match.all_players):
#                 block_data[player_name][GAMES] += 1
#         for player_name, player_stats in block_data.items():
#             if player_stats[GAMES] != 0:
#                 player_stats[WINRATE] = round(
#                     100 * player_stats[WINS] / player_stats[GAMES]
#                 )
#         return block_data

#     out_json = aggregate_matches(matches, cumulative_winrate)
#     json.dump(out_json, f, indent=2, default=str)
#     f.close()

# with open(
#     os.path.join(output_dir, "assists-per-game-over-time.json"), mode="w"
# ) as f:
#     out_json = {
#         player_name: {
#             assisted_name: [{ASSISTS_PER_STANDARD_GAME: 0, ASSISTS: 0, ROUNDS: 0}]
#             for assisted_name in PLAYER_NAMES
#         }
#         for player_name in PLAYER_NAMES
#     }

#     for match in matches:
#         for player_name in filter_players(match.all_players):
#             for assistant_name in filter_players(match.all_players):
#                 if match.players_in_same_team(player_name, assistant_name):
#                     if player_name == assistant_name:
#                         continue
#                     out_json[player_name][assistant_name][-1][ROUNDS] += len(
#                         match.rounds
#                     )
#         for _round in match.rounds:
#             # This will overwrite the round() function otherwise
#             for kill in _round.kills:
#                 if kill.killer_name == kill.victim_name:
#                     continue
#                 assisted_name = kill.killer_name
#                 if not is_player_of_interest(assisted_name):
#                     continue
#                 for player_name in filter_players(kill.assistants):
#                     out_json[player_name][assisted_name][-1][ASSISTS] += 1

#         for player_name in PLAYER_NAMES:
#             for assisted_name in PLAYER_NAMES:
#                 if out_json[player_name][assisted_name][-1][ROUNDS] != 0:
#                     out_json[player_name][assisted_name][-1][
#                         ASSISTS_PER_STANDARD_GAME
#                     ] = (
#                         round(
#                             10
#                             * 25
#                             * out_json[player_name][assisted_name][-1][ASSISTS]
#                             / out_json[player_name][assisted_name][-1][ROUNDS]
#                         )
#                         / 10
#                     )
#                 out_json[player_name][assisted_name].append(
#                     out_json[player_name][assisted_name][-1].copy()
#                 )

#     json.dump(out_json[SUSI][ANDY][:-1], f, indent=2)
#     f.close()
