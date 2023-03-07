import json
from threading import Lock, Thread
from urllib.parse import urlparse
import logging

from flask import Flask, request, current_app
from flask_cors import CORS

from generate_datasets import generate_datasets
from process_scrape import process_scrape
from scrape import scrape

app = Flask(__name__)
CORS(app)

# Locks scrape.json, data.json, out-min
scrape_lock = Lock()

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route("/api/dashboard")
def dashboard():
    datasets = [
        "assists-given-per-standard-game",
        "assists-received-per-standard-game",
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
    with open("out-min/dashboard.json", mode="r") as f:
        data = json.load(f)
        for dataset in datasets:
            out["_".join(dataset.split("-"))] = data[dataset]
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

    urls = []
    with open("./tracker-urls.txt", mode="r") as f:
        urls = [line.rstrip() for line in f]
        f.close()

    if url.geturl() in urls:
        return "Match is already included on the dashboard", 200

    if scrape_lock.locked():
        return (
            "Processing a previous add request; please try again in a few seconds",
            423,
        )

    scrape_lock.acquire()

    def process_url():
        try:
            app.logger.info(f"Processing {url.geturl()}")
            app.logger.info("Adding URL to tracker-urls.txt")
            with open("./tracker-urls.txt", mode="a") as f:
                f.write(f"\n{url.geturl()}")
                f.close()

            app.logger.info("Begin scraping")
            scrape()

            app.logger.info("Processing scraped data")
            process_scrape()

            app.logger.info("Making datasets")
            generate_datasets(output_dir="./out-min", minified=True)

            app.logger.info("Successfully updated dashboard.json")
        finally:
            scrape_lock.release()

    Thread(target=process_url).start()
    return "Request received", 202
