from constants import *
from Match import Match

from .DatasetGenerator import DatasetGenerator

MOST_RECENT_URL = "most_recent_url"


class MetaGenerator(DatasetGenerator):
    def __init__(self):
        self.filename = "meta.json"
        self.out_json = {
            MOST_RECENT_URL: "",
        }

    def accumulate(self, match: Match):
        self.out_json[MOST_RECENT_URL] = match.url

    def finalize(self, minified=False):
        return self.out_json
