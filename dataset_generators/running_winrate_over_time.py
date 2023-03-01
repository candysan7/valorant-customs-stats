from datetime import datetime, time, timedelta

from pytz import timezone

from config import PLAYER_NAMES
from constants import *
from Match import Match
from util import filter_players

from .DatasetGenerator import DatasetGenerator

BLOCK_END_TIME = "block_end_time"
DATA = "data"


class RunningWinrateOverTimeGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "running-winrate-over-time.json"
        self.out_json = []
        self.curr_block: list[Match] = []

        self.last_date = datetime.combine(
            datetime.today(), time.max, tzinfo=timezone("US/Pacific")
        )

        # TODO: Maybe time_increment and first curr_block_end_date should be actual inputs to the constructor
        self.block_length = timedelta(days=90)
        self.time_increment = timedelta(weeks=1)
        self.curr_block_end_date = datetime.combine(
            datetime(year=2022, month=10, day=9),
            time.max,
            tzinfo=timezone("US/Pacific"),
        )
        self.curr_block_start_date = self.curr_block_end_date - self.block_length

    def accumulate(self, match: Match):
        if len(self.out_json) == 0:
            self.out_json.append(
                {
                    BLOCK_END_TIME: self.curr_block_end_date.isoformat(),
                    DATA: {
                        player_name: {WINRATE: None, WINS: 0, GAMES: 0}
                        for player_name in PLAYER_NAMES
                    },
                }
            )

        # Blocks look like (curr_block_start_date, curr_block_end_date]
        while match.time > self.curr_block_end_date:
            self.curr_block_start_date += self.time_increment
            self.curr_block_end_date += self.time_increment

            prev_block = self.out_json[-1]
            next_block = {
                BLOCK_END_TIME: self.curr_block_end_date.isoformat(),
                DATA: {
                    player_name: {
                        WINRATE: None,
                        WINS: prev_block[DATA][player_name][WINS],
                        GAMES: prev_block[DATA][player_name][GAMES],
                    }
                    for player_name in PLAYER_NAMES
                },
            }

            # Remove data from matches that are too old for this block
            while (
                len(self.curr_block) > 0
                and self.curr_block[0].time <= self.curr_block_start_date
            ):
                removed_match = self.curr_block.pop(0)
                for winner_name in filter_players(removed_match.winning_players):
                    next_block[DATA][winner_name][WINS] -= 1
                for player_name in filter_players(removed_match.all_players):
                    next_block[DATA][player_name][GAMES] -= 1

            self.out_json.append(next_block)

        block_data = self.out_json[-1]
        for winner_name in filter_players(match.winning_players):
            block_data[DATA][winner_name][WINS] += 1
        for player_name in filter_players(match.all_players):
            block_data[DATA][player_name][GAMES] += 1

        self.curr_block.append(match)

    def finalize(self, minified=False):
        if datetime.fromisoformat(self.out_json[-1][BLOCK_END_TIME]) > self.last_date:
            self.out_json.pop()

        # The last block corresponds to today
        prev_block = self.out_json[-1]
        next_block = {
            BLOCK_END_TIME: self.last_date.isoformat(),
            DATA: {
                player_name: {
                    WINRATE: None,
                    WINS: prev_block[DATA][player_name][WINS],
                    GAMES: prev_block[DATA][player_name][GAMES],
                }
                for player_name in PLAYER_NAMES
            },
        }

        last_start_date = self.last_date - self.block_length
        while len(self.curr_block) > 0 and self.curr_block[0].time <= last_start_date:
            removed_match = self.curr_block.pop(0)
            for winner_name in filter_players(removed_match.winning_players):
                next_block[DATA][winner_name][WINS] -= 1
            for player_name in filter_players(removed_match.all_players):
                next_block[DATA][player_name][GAMES] -= 1

        self.out_json.append(next_block)

        for block_data in self.out_json:
            for _, player_stats in block_data[DATA].items():
                if player_stats[GAMES] != 0:
                    player_stats[WINRATE] = round(
                        100 * player_stats[WINS] / player_stats[GAMES]
                    )

                if minified:
                    del player_stats[WINS]
                    del player_stats[GAMES]

        return self.out_json
