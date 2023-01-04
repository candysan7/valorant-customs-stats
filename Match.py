from datetime import datetime


class Player:
    def __init__(self, player_json):
        self.player_name: str = player_json["player_name"]
        self.agent: str = player_json["agent"]
        self.average_combat_score: int = player_json["average_combat_score"]
        self.kills: int = player_json["kills"]
        self.deaths: int = player_json["deaths"]
        self.assists: int = player_json["assists"]
        self.kill_deaths: float = player_json["kill_deaths"]
        self.kill_assist_survive_traded: int = player_json["kill_assist_survive_traded"]
        self.first_kills: int = player_json["first_kills"]
        self.first_deaths: int = player_json["first_deaths"]
        self.multi_kills: int = player_json["multi_kills"]
        self.econ: int = player_json["econ"]

    def __hash__(self):
        return self.player_name.__hash__()


class Match:
    def __init__(self, match_json):
        # match_json.time looks like "10/11/22, 9:08 PM"
        self.time: datetime = datetime.fromisoformat(match_json["time"])
        self.url: str = match_json["url"]
        self.map: str = match_json["map"]
        self.score_red: int = match_json["score_red"]
        self.score_blue: int = match_json["score_blue"]
        self.team_red: dict[str, Player] = {
            player_json["player_name"]: Player(player_json)
            for player_json in match_json["team_red"]
        }
        self.team_blue: dict[str, Player] = {
            player_json["player_name"]: Player(player_json)
            for player_json in match_json["team_blue"]
        }

        self.all_players = self.team_red | self.team_blue
        if self.score_red > self.score_blue:
            self.winning_players: dict[str, Player] = self.team_red
            self.losing_players: dict[str, Player] = self.team_blue
        else:
            self.winning_players: dict[str, Player] = self.team_blue
            self.losing_players: dict[str, Player] = self.team_red

    def player_did_play(self, player_name):
        return player_name in self.all_players

    def all_players_did_play(self, *PLAYER_NAMES):
        return all([self.player_did_play(player_name) for player_name in PLAYER_NAMES])

    def player_did_win(self, player_name):
        return player_name in self.winning_players

    def all_players_did_win(self, *PLAYER_NAMES):
        return all([self.player_did_win(player_name) for player_name in PLAYER_NAMES])

    def player_did_lose(self, player_name):
        return player_name in self.losing_players

    def all_players_did_lose(self, *PLAYER_NAMES):
        return all([self.players_did_lose(player_name) for player_name in PLAYER_NAMES])

    def players_in_same_team(self, *PLAYER_NAMES):
        return all([player_name in self.team_a for player_name in PLAYER_NAMES]) or all(
            [player_name in self.team_b for player_name in PLAYER_NAMES]
        )
