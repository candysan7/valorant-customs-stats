import json
import os
from typing import TypeAlias

from Match import Match

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class DatasetGenerator:
    def __init__(self, name: str):
        self.name = name
        self.out_json = None
        pass

    def accumulate(self, match: Match) -> None:
        "How the generator should process each match. For example, increase counts on its out_json dict."
        pass

    def finalize(self, minified=False) -> JSON:
        "Should be run after each match has been accumulated. For example, a generator may compute rates from its counts."
        pass

    def generate(self, output_dir, minified=False) -> None:
        "Dump out_json into output_dir/filename."
        indent = 2
        separators = None
        if minified:
            indent = None
            separators = (",", ":")

        with open(os.path.join(output_dir, f"{self.name}.json"), mode="w") as f:
            json.dump(self.out_json, f, indent=indent, separators=separators)
            f.close()
