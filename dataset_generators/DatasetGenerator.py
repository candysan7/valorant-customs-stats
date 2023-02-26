import json
import os
from Match import Match


class DatasetGenerator:
    def __init__(self, filename):
        self.out_json = None
        pass

    def accumulate(self, match: Match):
        pass

    def finalize(self, minified=False):
        pass

    def generate(self, output_dir, minified=False):
        indent = 2
        separators = None
        if minified:
            indent = None
            separators = (",", ":")

        with open(os.path.join(output_dir, self.filename), mode="w") as f:
            json.dump(self.out_json, f, indent=indent, separators=separators)
            f.close()
