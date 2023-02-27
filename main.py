from io import TextIOWrapper
import json, os.path, sys

from Match import Match
from dataset_generators import *


matches: list[Match] = []
with open("./data.json", mode="r") as f:
    data = json.load(f)
    # data.json is sorted in process_scrape.py
    # matches = sorted([Match(match_json) for match_json in data], key=lambda m: m.time)
    matches = [Match(match_json) for match_json in data]
    f.close()

if __name__ == "__main__":
    minified = False
    output_dir = "./out"
    if len(sys.argv) > 1 and sys.argv[1] == "--minified":
        minified = True
        output_dir = "./out-min"

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

    for match in matches:
        for generator in generators:
            generator.accumulate(match)

    for generator in generators:
        generator.finalize(minified=minified)
        generator.generate(output_dir=output_dir, minified=minified)

    with open(os.path.join(output_dir, "data-frame-friendly.json"), mode="w") as f:
        out_json = {i: match_json for i, match_json in enumerate(data)}
        indent = 2
        separators = None
        if minified:
            indent = None
            separators = (",", ":")
        json.dump(out_json, f, indent=indent, separators=separators)
        f.close()
