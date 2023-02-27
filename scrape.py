import json
import os.path
import time
from random import uniform
from urllib.parse import urlparse

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

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
    print(f"[{i}/{len(urls)}]: {url}")
    while True:
        try:
            api_url = f"https://api.tracker.gg/api/v2/valorant/standard/matches/{urlparse(url).path.split('/')[-1]}"
            driver.get(api_url)
            time.sleep(0.5 + uniform(-0.125, 0.125))

            match_json = json.loads(driver.find_element(By.CSS_SELECTOR, "pre").text)[
                "data"
            ]
            match_json["tracker_url"] = url

            matches.append(match_json)
            break
        except Exception as e:
            print(e)
            continue


print("Saving...")
with open("./scrape.json", mode="w") as f:
    json.dump(matches, f, separators=(",", ":"))
    f.close()
print("Done")

driver.close()
