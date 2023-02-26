from Match import Match
from constants.valorant import *
from .DatasetGenerator import DatasetGenerator


class MapsGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "maps.json"
        self.out_json = {map: 0 for map in MAP_NAMES}

    def accumulate(self, match: Match):
        self.out_json[match.map] += 1

    def finalize(self, minified=False):
        return self.out_json
