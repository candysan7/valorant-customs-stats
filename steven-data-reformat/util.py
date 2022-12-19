from datetime import datetime, timedelta
from typing import Callable

from Match import Match
from constants import player_names


class IntervalData:
    def __init__(self, block_start_time, data):
        self.block_start_time: datetime = block_start_time
        self.data = data


def aggregate_matches(
    matches: list[Match],
    # Second argument is the output from the previous block; None if it's the first block
    aggregate_fn: Callable[[list[Match], any], any],
    # Default first time is October 3rd, 2022, which is the week before the first tracked customs
    start_date: datetime = datetime(year=2022, month=10, day=3),
    interval: timedelta = timedelta(days=60),
) -> list[IntervalData]:
    """Aggregate matches into specified intervals. `matches` must be sorted from oldest to newest."""
    out = []

    curr_block_start_i = 0
    curr_block_start_date = start_date
    curr_block_end_date = start_date + interval

    i = 0
    while i <= len(matches):
        # Current time block is the time interval [curr_block_start_date, curr_block_end_date)
        # If we reach the end of the list or matches[i] is outside the current time block
        if i == len(matches) or matches[i].time >= curr_block_end_date:
            out.append(
                {
                    "block_start_time": curr_block_start_date,
                    "data": aggregate_fn(
                        matches[curr_block_start_i:i],
                        out[-1] if len(out) > 0 else None,
                    ),
                }
            )
            curr_block_start_date = curr_block_end_date
            curr_block_end_date = curr_block_start_date + interval
            curr_block_start_i = i
        i += 1

    return out


def filter_players(player_list):
    return list(filter(lambda player_name: player_name in player_names, player_list))
