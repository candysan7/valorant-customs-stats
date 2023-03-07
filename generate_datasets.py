import json
import os.path
import sys

from dataset_generators import *
from Match import Match


def generate_datasets(output_dir, minified=False):
    matches: list[Match] = []
    with open("./data.json", mode="r") as f:
        data = json.load(f)
        # data.json is sorted in process_scrape.py
        # matches = sorted([Match(match_json) for match_json in data], key=lambda m: m.time)
        matches = [Match(match_json) for match_json in data]
        f.close()

    generators: list[DatasetGenerator] = [
        AssistsGivenPerStandardGameGenerator(),
        AssistsReceivedPerStandardGameGenerator(),
        EasiestMatchupsGenerator(),
        IndividualGenerator(),
        MapsGenerator(),
        MetaGenerator(),
        RecentLobbyWinRatesGenerator(),
        RolesGenerator(),
        RunningWinrateOverTimeGenerator(),
        TeamSynergyDataGenerator(),
        TeammateSynergyGenerator(),
        WallOfShameGenerator(),
    ]

    all_json = {}

    for match in matches:
        for generator in generators:
            generator.accumulate(match)

    for generator in generators:
        all_json[generator.name] = generator.finalize(minified=minified)

        # Each dataset gets its own file with the below line
        # generator.generate(output_dir=output_dir, minified=minified)

    indent = 2
    separators = None
    if minified:
        indent = None
        separators = (",", ":")

    with open(os.path.join(output_dir, "dashboard.json"), mode="w") as f:
        json.dump(all_json, f, indent=indent, separators=separators)
        f.close()

    # with open(os.path.join(output_dir, "data-frame-friendly.json"), mode="w") as f:
    #     out_json = {i: match_json for i, match_json in enumerate(data)}
    #     json.dump(out_json, f, indent=indent, separators=separators)
    #     f.close()


if __name__ == "__main__":
    minified = False
    output_dir = "./out"
    if len(sys.argv) > 1 and sys.argv[1] == "--minified":
        minified = True
        output_dir = "./out-min"
    generate_datasets(output_dir=output_dir, minified=minified)
