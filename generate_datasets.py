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

    dashboard_generators: list[DatasetGenerator] = [
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
    ]
    wall_of_shame_generator = WallOfShameGenerator()
    teammate_synergy_data_generator = TeamSynergyDataGenerator()

    all_generators = dashboard_generators + [
        wall_of_shame_generator,
        teammate_synergy_data_generator,
    ]

    for match in matches:
        for generator in all_generators:
            generator.accumulate(match)

    # Data for api/dashboard
    dashboard_json = {}
    for generator in dashboard_generators:
        dashboard_json["_".join(generator.name.split("-"))] = generator.finalize(
            minified=minified
        )

    # Data for api/wall-of-shame
    wall_of_shame_generator.finalize()
    wall_of_shame_generator.generate(output_dir=output_dir, minified=minified)

    # Data for training one of Andy's balancing algorithms
    teammate_synergy_data_generator.finalize()
    teammate_synergy_data_generator.generate(output_dir=output_dir, minified=minified)

    indent = 2
    separators = None
    if minified:
        indent = None
        separators = (",", ":")

    with open(os.path.join(output_dir, "dashboard.json"), mode="w") as f:
        json.dump(dashboard_json, f, indent=indent, separators=separators)
        f.close()

    # with open(os.path.join(output_dir, "data-frame-friendly.json"), mode="w") as f:
    #     out_json = {i: match_json for i, match_json in enumerate(data)}
    #     json.dump(out_json, f, indent=indent, separators=separators)
    #     f.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--minified":
        generate_datasets(output_dir="./out-min", minified=True)
        exit()

    output_dir = "./out"

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
        RunningWinrateOverTimeGenerator(),
        TeammateSynergyGenerator(),
        WallOfShameGenerator(),
    ]

    for match in matches:
        for generator in generators:
            generator.accumulate(match)

    for generator in generators:
        generator.finalize()
        generator.generate(output_dir=output_dir)

    with open(os.path.join(output_dir, "data-frame-friendly.json"), mode="w") as f:
        out_json = {i: match_json for i, match_json in enumerate(data)}
        json.dump(out_json, f)
        f.close()
