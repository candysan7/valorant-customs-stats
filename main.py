import csv
from datetime import date, timedelta


class Match:
    def __init__(self, date, map, winners, losers):
        self.date = date
        self.map = map
        self.winners = winners
        self.losers = losers

    def player_did_win(self, player):
        return player in self.winners

    def player_did_lose(self, player):
        return player in self.losers

    def player_did_play(self, player):
        return player in self.winners or player in self.losers


matches = []
players = set()
maps = set()

with open(file="./data.csv", mode="r") as data:
    reader = csv.reader(data)
    next(reader)
    for row in reader:
        matches.append(Match(row[0], row[1], set(row[2:7]), set(row[7:])))
        maps.add(row[1])
        for player in row[2:]:
            if player != "":
                players.add(player)
data.close()

matches = sorted(matches, key=lambda x: date.fromisoformat(x.date))
players = sorted(list(players))
maps = sorted(list(maps))

with open("./individual.csv", mode="w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["player", "winrate", "wins", "games"])
    for player in players:
        wins = 0
        total = 0
        for match in matches:
            if match.player_did_play(player):
                total += 1
            if match.player_did_win(player):
                wins += 1
        else:
            writer.writerow(
                [player, round(100 * wins/total), wins, total])
out.close()

with open("./teammate-synergy.csv", mode="w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["player"] + players * 2)
    for player1 in players:
        row_start = [player1]
        row_percentage = []
        row_fraction = []
        for player2 in players:
            pair = (player1, player2)
            wins = 0
            total = 0
            for match in matches:
                if all([match.player_did_lose(player) for player in pair]):
                    total += 1
                if all([match.player_did_win(player) for player in pair]):
                    total += 1
                    wins += 1
            if total == 0:
                row_percentage += [""]
                row_fraction += [""]
            else:
                row_percentage += [round(100 * wins / total)]
                row_fraction += [f"{wins}/{total}"]
        writer.writerow(row_start + row_percentage + row_fraction)
out.close()

with open("./easiest-matchups.csv", mode="w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["player"] + players * 2)
    for left in players:
        row_start = [left]
        row_percentage = []
        row_fraction = []
        for top in players:
            pair = (left, top)
            wins = 0
            total = 0
            for match in matches:
                if match.player_did_win(left) and match.player_did_lose(top):
                    total += 1
                if match.player_did_lose(left) and match.player_did_win(top):
                    total += 1
                    wins += 1
            if total == 0:
                row_percentage += [""]
                row_fraction += [""]
            else:
                row_percentage += [round(100 * wins / total)]
                row_fraction += [f"{wins}/{total}"]
        writer.writerow(row_start + row_percentage + row_fraction)
out.close()

with open("./maps.csv", mode="w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["map", "percentage", "games"])
    total = len(matches)
    for map in maps:
        count = 0
        for match in matches:
            if match.map == map:
                count += 1
        writer.writerow([map, round(100 * count / total), count])
out.close()

with open("./winrate-over-time.csv", mode="w", newline="") as out:
    writer = csv.writer(out)

    # { player: [wins1, total1, wins2, total2, ...] }
    player_to_stats = {player: [] for player in players}

    # Two week blocks; first time is October 3rd, 2022, which is the week before the first recorded customs
    start = date(year=2022, month=10, day=3)
    end = start + timedelta(weeks=2)
    header = ["player", start]

    start_i = 0
    i = 0
    while i <= len(matches):
        # Current window is [current date, end); corresponds to [start_i, i)
        if i == len(matches) or date.fromisoformat(matches[i].date) >= end:
            # Initialize the next set of stats
            for player in players:
                player_to_stats[player] += [[0, 0]]

            # Update the next set of stats
            for match in matches[start_i:i]:
                for player in match.winners | match.losers:
                    if player == "":
                        continue
                    player_to_stats[player][-1][1] += 1
                for player in match.winners:
                    if player == "":
                        continue
                    player_to_stats[player][-1][0] += 1

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

with open("./cumulative-winrate-over-time.csv", mode="w", newline="") as out:
    writer = csv.writer(out)

    # { player: [wins1, total1, wins2, total2, ...] }
    player_to_stats = {player: [] for player in players}

    # Two week blocks; first time is October 3rd, 2022, which is the week before the first recorded customs
    start = date(year=2022, month=10, day=3)
    end = start + timedelta(weeks=2)
    header = ["player", start]

    start_i = 0
    i = 0
    while i <= len(matches):
        # Current window is [current date, end); corresponds to [start_i, i)
        if i == len(matches) or date.fromisoformat(matches[i].date) >= end:
            # Initialize the next set of stats
            for player in players:
                if len(player_to_stats[player]) == 0:
                    player_to_stats[player] += [[0, 0]]
                else:
                    player_to_stats[player] += [player_to_stats[player][-1].copy()]

            # Update the next set of stats
            for match in matches[start_i:i]:
                for player in match.winners | match.losers:
                    if player == "":
                        continue
                    player_to_stats[player][-1][1] += 1
                for player in match.winners:
                    if player == "":
                        continue
                    player_to_stats[player][-1][0] += 1

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

# print("P(winning)")
# for player in players:
#     print(f"{player:>12}", end="")
#     wins = 0
#     total = 0
#     for match in matches:
#         if match.player_did_play(player):
#             total += 1
#         if match.player_did_win(player):
#             wins += 1
#     if total == 0:
#         print(f"{'N/A':>12}")
#     else:
#         print(f"{f'{wins / total:>6.0%}':>12}")
# print()

# print("P(top wins | top, left on the same team)")
# print(" " * 12, end="")
# for player in players:
#     print(f"{player:>12}", end="")
# print()

# for player1 in players:
#     print(f"{player1:>12}", end="")
#     for player2 in players:
#         pair = (player1, player2)
#         wins = 0
#         total = 0
#         for match in matches:
#             if all([match.player_did_lose(player) for player in pair]):
#                 total += 1
#             if all([match.player_did_win(player) for player in pair]):
#                 total += 1
#                 wins += 1
#         if total == 0:
#             print(f"{'N/A':>12}", end="")
#         else:
#             print(f"{f'{wins / total:>6.0%}':>12}", end="")
#     print()
# print()

# print("P(top wins | top, left on opposite teams)")
# print(" " * 12, end="")
# for player in players:
#     print(f"{player:>12}", end="")
# print()

# for left in players:  # left
#     print(f"{left:>12}", end="")
#     for top in players:  # top
#         pair = (left, top)
#         wins = 0
#         total = 0
#         for match in matches:
#             if match.player_did_win(left) and match.player_did_lose(top):
#                 total += 1
#             if match.player_did_lose(left) and match.player_did_win(top):
#                 total += 1
#                 wins += 1
#         if total == 0:
#             print(f"{'N/A':>12}", end="")
#         else:
#             print(f"{f'{wins / total:>6.0%}':>12}", end="")
#     print()
