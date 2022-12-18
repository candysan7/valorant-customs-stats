from Match import Match

import csv
from datetime import date, timedelta


matches = []
players = set()
maps = set()

with open(file="./data.csv", mode="r") as data:
    reader = csv.reader(data)
    next(reader)
    for row in reader:
        matches.append(Match(date.fromisoformat(row[0]),
                             row[1], set(row[2:7]), set(row[7:])))
        maps.add(row[1])
        for player in row[2:]:
            if player != "":
                players.add(player)
data.close()

matches = sorted(matches, key=lambda x: x.date)
players = sorted(list(players))
maps = sorted(list(maps))


if __name__ == "__main__":
    with open("./out/individual.csv", mode="w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["player", "winrate", "wins", "games"])
        for player in players:
            wins = len(
                [match for match in matches if match.player_did_win(player)])
            total = len(
                [match for match in matches if match.player_did_play(player)])
            writer.writerow(
                [player, round(100 * wins/total), wins, total])
        out.close()

    with open("./out/teammate-synergy.csv", mode="w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["player"] + players * 2)
        for teammate in players:
            row_start, row_percentage, row_fraction = [teammate], [], []
            for player in players:
                wins = len(
                    [match for match in matches
                     if all([match.player_did_win(teammate), match.player_did_win(player)])]
                )
                total = wins + len(
                    [match for match in matches
                     if all([match.player_did_lose(teammate), match.player_did_lose(player)])]
                )
                if total == 0:
                    row_percentage += [""]
                    row_fraction += [""]
                else:
                    row_percentage += [round(100 * wins / total)]
                    row_fraction += [f"{wins}/{total}"]
            writer.writerow(row_start + row_percentage + row_fraction)
        out.close()

    with open("./out/easiest-matchups.csv", mode="w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["player"] + players * 2)
        for opponent in players:
            row_start, row_percentage, row_fraction = [opponent], [], []
            for player in players:
                wins = len(
                    [match for match in matches
                     if all([match.player_did_lose(opponent), match.player_did_win(player)])]
                )
                total = wins + len(
                    [match for match in matches
                     if all([match.player_did_win(opponent), match.player_did_lose(player)])]
                )
                if total == 0:
                    row_percentage += [""]
                    row_fraction += [""]
                else:
                    row_percentage += [round(100 * wins / total)]
                    row_fraction += [f"{wins}/{total}"]
            writer.writerow(row_start + row_percentage + row_fraction)
        out.close()

    with open("./out/maps.csv", mode="w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["map", "percentage", "games"])
        total = len(matches)
        for map in maps:
            count = len([match for match in matches if match.map == map])
            writer.writerow([map, round(100 * count / total), count])
        out.close()

    with open("./out/winrate-over-time.csv", mode="w", newline="") as out:
        writer = csv.writer(out)

        # { player: [wins1, total1, wins2, total2, ...] }
        player_to_stats = {player: [] for player in players}

        # Two week blocks; first time is October 3rd, 2022, which is the week before the first recorded customs
        start = date(year=2022, month=10, day=3)
        end = start + timedelta(weeks=2)
        header = ["player", start]

        start_i, i = 0, 0
        while i <= len(matches):
            # Current window is [current date, end); corresponds to [start_i, i)
            if i == len(matches) or matches[i].date >= end:
                # Initialize the next set of stats
                for player in players:
                    player_to_stats[player] += [[0, 0]]

                # Update the next set of stats
                for match in matches[start_i:i]:
                    for player in match.winners:
                        player_to_stats[player][-1][0] += 1
                    for player in match.winners | match.losers:
                        player_to_stats[player][-1][1] += 1

                start = end
                end = start + timedelta(weeks=2)
                header += [start]

                start_i = i

            i += 1

        writer.writerow(header)
        for player in players:
            writer.writerow([player] + [round(100 * x[0]/x[1]) if x[1]
                            != 0 else "" for x in player_to_stats[player]])
        out.close()

    with open("./out/cumulative-winrate-over-time.csv", mode="w", newline="") as out:
        writer = csv.writer(out)

        # { player: [wins1, total1, wins2, total2, ...] }
        player_to_stats = {player: [] for player in players}

        # Two week blocks; first time is October 3rd, 2022, which is the week before the first recorded customs
        start = date(year=2022, month=10, day=3)
        end = start + timedelta(weeks=2)
        header = ["player", start]

        start_i, i = 0, 0
        while i <= len(matches):
            # Current window is [current match date, end); corresponds to [start_i, i)
            if i == len(matches) or matches[i].date >= end:
                # Initialize the next set of stats
                for player in players:
                    if len(player_to_stats[player]) == 0:
                        player_to_stats[player] += [[0, 0]]
                    else:
                        player_to_stats[player] += [player_to_stats[player][-1].copy()]

                # Update the next set of stats
                for match in matches[start_i:i]:
                    for player in match.winners:
                        player_to_stats[player][-1][0] += 1
                    for player in match.winners | match.losers:
                        player_to_stats[player][-1][1] += 1

                start = end
                end = start + timedelta(weeks=2)
                header += [start]

                start_i = i

            i += 1

        writer.writerow(header)
        for player in players:
            writer.writerow([player] + [round(100 * x[0]/x[1]) if x[1] != 0 else ""
                                        for x in player_to_stats[player]])
        out.close()
