import json
from flask import Flask, abort, request
from flask_cors import CORS

from urllib.parse import urlparse

from generate_datasets import generate_datasets

app = Flask(__name__)
CORS(app)


@app.route("/api/dashboard")
def dashboard():
    datasets = [
        "assists-given-per-standard-game",
        "assists-received-per-standard-game",
        "data-frame-friendly",
        "easiest-matchups",
        "individual",
        "maps",
        "meta",
        "recent-lobby-win-rates",
        "roles",
        "running-winrate-over-time",
        "team-synergy-data",
        "teammate-synergy",
    ]

    out = {}
    for dataset in datasets:
        with open(f"out-min/{dataset}.json", mode="r") as f:
            out["_".join(dataset.split("-"))] = json.load(f)
            f.close()
    return out


@app.route("/api/wall-of-shame")
def wall_of_shame():
    out = {}
    with open("out-min/wall-of-shame.json", mode="r") as f:
        out = json.load(f)
        f.close()
    return out


@app.route("/api/add", methods=["PUT"])
def add_url():
    if "url" not in request.form:
        return "Missing tracker url", 401

    # E.g., https://tracker.gg/valorant/match/770f73b1-95db-48ce-94f3-809d5cb5b00d
    url = urlparse(request.form["url"])
    if url.hostname != "tracker.gg":
        return "Invalid tracker url", 401

    print(url)

    urls = []
    with open("./tracker-urls.txt", mode="r") as f:
        urls = [line.rstrip() for line in f]
        f.close()

    if url.geturl() in urls:
        return "Match is already included on the dashboard", 200

    with open("./tracker-urls.txt", mode="a") as f:
        f.write(f"\n{url.geturl()}")
        f.close()

    generate_datasets(output_dir="./out-min", minified=True)
    return "Success"


app.run()
