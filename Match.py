from datetime import date


class Match:
    def __init__(self, date: date, map: str, winners: set[str], losers: set[str]):
        self.date = date
        self.map = map

        self.winners = winners
        if "" in self.winners:
            self.winners.remove("")
        self.losers = losers
        if "" in self.losers:
            self.losers.remove("")

    def player_did_win(self, player):
        return player in self.winners

    def player_did_lose(self, player):
        return player in self.losers

    def player_did_play(self, player):
        return player in self.winners | self.losers
