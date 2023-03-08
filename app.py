import atexit
import json
import logging
import time
from threading import Thread
from multiprocessing import Lock
from urllib.parse import urlparse

import jsonlines
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_cors import CORS

from generate_datasets import generate_datasets
from process_scrape import process_scrape
from scrape import scrape_url

# Makes URL processing atomic
url_processing_lock = Lock()

app = Flask(__name__)
CORS(app)

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

# TODO: Cron job

#### Routes
@app.route("/api/dashboard")
def dashboard():
    out = {}
    with open("out-min/dashboard.json", mode="r") as f:
        data: dict = json.load(f)
        for name, dataset in data.items():
            out["_".join(name.split("-"))] = dataset
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

    if not url_processing_lock.acquire(block=False):
        return (
            "Currently procesing a URL; please try again in a few seconds",
            423,
        )

    urls = []
    with open("./tracker-urls.txt", mode="r") as f:
        urls = [line.rstrip() for line in f]
        f.close()

    if url.geturl() in urls:
        url_processing_lock.release()
        return "Match is already included on the dashboard", 200

    Thread(
        target=process_url,
        kwargs={"lock": url_processing_lock, "url": url.geturl()},
    ).start()
    return "Request received", 202


def process_url(lock, url: str):
    try:
        app.logger.info(f"Processing {url}")

        app.logger.info("Begin scraping")
        match_json = scrape_url(url)

        app.logger.info("Updating scrape.json")
        with jsonlines.open("./scrape.jsonl", mode="a") as f:
            f.write(match_json)
            f.close()

        app.logger.info("Adding URL to tracker-urls.txt")
        with open("./tracker-urls.txt", mode="a") as f:
            f.write(f"\n{url}")
            f.close()

        app.logger.info("Processing scraped data")
        process_scrape()

        app.logger.info("Updating out-min")
        generate_datasets(output_dir="./out-min", minified=True)

        app.logger.info("Successfully processed URL")
    except Exception as e:
        app.logger.exception("Failed to process URL")
    finally:
        lock.release()
