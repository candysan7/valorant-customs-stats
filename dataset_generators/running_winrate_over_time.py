from .DatasetGenerator import DatasetGenerator
from util import filter_players
from Match import Match
from constants.misc import *
from constants.players import *

from datetime import datetime, timedelta, time
from pytz import timezone

BLOCK_END_TIME = "block_end_time"
DATA = "data"


class RunningWinrateOverTimeGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "running-winrate-over-time.json"
        self.out_json = []

        self.last_date = datetime.combine(
            datetime.today(), time.max, tzinfo=timezone("US/Pacific")
        )

        # TODO: Maybe time_increment and first curr_block_end_date should be actual inputs to the constructor
        self.time_increment = timedelta(weeks=1)
        self.curr_block_end_date = datetime.combine(
            datetime(year=2022, month=10, day=9),
            time.max,
            tzinfo=timezone("US/Pacific"),
        )
        self.curr_block_start_date = self.curr_block_end_date - timedelta(days=90)

    def accumulate(self, match: Match):
        # Blocks look like (curr_block_start_date, curr_block_end_date]
        if len(self.out_json) == 0 or match.time > self.curr_block_end_date:
            if match.time > self.curr_block_end_date:
                self.curr_block_start_date += self.time_increment
                self.curr_block_end_date += self.time_increment

            self.out_json.append(
                {
                    BLOCK_END_TIME: self.curr_block_end_date,
                    DATA: {
                        player_name: {WINRATE: None, WINS: 0, GAMES: 0}
                        for player_name in PLAYER_NAMES
                    },
                }
            )

        block_data = self.out_json[-1]

        for winner_name in filter_players(match.winning_players):
            block_data[DATA][winner_name][WINS] += 1
        for player_name in filter_players(match.all_players):
            block_data[DATA][player_name][GAMES] += 1

    def finalize(self, minified=False):
        for block_data in self.out_json:
            block_data[BLOCK_END_TIME] = block_data[BLOCK_END_TIME].isoformat()
            for _, player_stats in block_data[DATA].items():
                if player_stats[GAMES] != 0:
                    player_stats[WINRATE] = round(
                        100 * player_stats[WINS] / player_stats[GAMES]
                    )

                if minified:
                    del player_stats[WINS]
                    del player_stats[GAMES]

        self.out_json[-1][BLOCK_END_TIME] = self.last_date.isoformat()
        return self.out_json
