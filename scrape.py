import json
import os.path
import time
from random import uniform
from urllib.parse import urlparse

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def scrape_url(url: str, driver=None):
    if driver is None:
        options = uc.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.headless = True
        driver = uc.Chrome(options=options)

    api_url = f"https://api.tracker.gg/api/v2/valorant/standard/matches/{urlparse(url).path.split('/')[-1]}"
    driver.get(api_url)

    match_json = json.loads(driver.find_element(By.CSS_SELECTOR, "pre").text)["data"]
    match_json["tracker_url"] = url
    return match_json


if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.headless = True
    driver = uc.Chrome(options=options)

    # Starting from 10/11/22
    urls = []
    if os.path.exists("./tracker-urls.txt"):
        with open("./tracker-urls.txt", mode="r") as f:
            urls = [line.rstrip() for line in f]
        f.close()

    matches = []
    if os.path.exists("./scrape.json"):
        with open("./scrape.json", mode="r") as f:
            matches = json.load(f)
        f.close()

    for match in matches:
        if match["tracker_url"] in urls:
            urls.remove(match["tracker_url"])

    for i, url in enumerate(urls, start=1):
        print(
            f"[{'0' if i <= 9 and len(urls) >= 10 else ''}{i}/{len(urls)}]: Scraping {url}... ",
            end="",
        )
        retries = 5
        while retries > 0:
            retries -= 1
            try:
                time.sleep(0.5 + uniform(-0.125, 0.125))
                match_json = scrape_url(url, driver=driver)
                matches.append(match_json)

                print("Success")
                break
            except Exception as e:
                if retries == 0:
                    print("Failed")
                    break
                print(e)
                continue

    print("Saving...")
    with open("./scrape.json", mode="w") as f:
        json.dump(matches, f, separators=(",", ":"))
        f.close()
    print("Done")

    driver.close()
