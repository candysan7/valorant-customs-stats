import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


urls = ["https://tracker.gg/valorant/match/bf09a9fe-8f9f-41b5-bcbb-6b8301ab26d7?handle=aylindsay%230613",
        "https://tracker.gg/valorant/match/e8380c75-fe6c-42d6-84f3-78d3f6f88fc4?handle=aylindsay%230613",
        "https://tracker.gg/valorant/match/6c87a77f-488e-4a8a-a0ad-9aa0cd1b808a?handle=aylindsay%230613",
        "https://tracker.gg/valorant/match/bef040b2-e3b3-42b3-8c6b-bf4af9e5c9d7?handle=aylindsay%230613"]

username_to_name = {
    "RhythmKing": "cade",
    "Candysan": "andy",
    "tangy": "tang",
    "chushberry": "sophie",
    "BigBoiB": "brandon",
    "Sequential": "sequential",
    "Selintt": "steve",
    "aylindsay": "lindsey",

    "ChzGorditaCrunch": "darwin",
    "Mirabel Madrigal": "darwin",
    "Jeff Probst": "darwin",

    "brianwoohoo": "brian",
    "bot001341": "josh",
    "sun": "sun",
    "Tyblerone": "yang",
    "youngsmasher": "steven",
    "SusTwins": "susi",
    "danielscutiegf": "susu"
}

image_url_to_agent = {
    "https://titles.trackercdn.com/valorant-api/agents/95b78ed7-4637-86d9-7e41-71ba8c293152/displayicon.png": "Harbor",
    "https://titles.trackercdn.com/valorant-api/agents/dade69b4-4f5a-8528-247b-219e5a1facd6/displayicon.png": "Fade",
    "https://titles.trackercdn.com/valorant-api/agents/bb2a4828-46eb-8cd1-e765-15848195d751/displayicon.png": "Neon",
    "https://titles.trackercdn.com/valorant-api/agents/22697a3d-45bf-8dd7-4fec-84a9e28c69d7/displayicon.png": "Chamber",
    "https://titles.trackercdn.com/valorant-api/agents/6f2a04ca-43e0-be17-7f36-b3908627744d/displayicon.png": "Skye",
    "https://titles.trackercdn.com/valorant-api/agents/7f94d92c-4234-0a36-9646-3a87eb8b5c89/displayicon.png": "Yoru",
    "https://titles.trackercdn.com/valorant-api/agents/41fb69c1-4189-7b37-f117-bcaf1e96f1bf/displayicon.png": "Astra",
    "https://titles.trackercdn.com/valorant-api/agents/601dbbe7-43ce-be57-2a40-4abd24953621/displayicon.png": "KAY/O",
    "https://titles.trackercdn.com/valorant-api/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png": "Phoenix",
    "https://titles.trackercdn.com/valorant-api/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png": "Raze",
    "https://titles.trackercdn.com/valorant-api/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png": "Brimstone",
    "https://titles.trackercdn.com/valorant-api/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png": "Jett",
    "https://titles.trackercdn.com/valorant-api/agents/569fdd95-4d10-43ab-ca70-79becc718b46/displayicon.png": "Sage",
    "https://titles.trackercdn.com/valorant-api/agents/707eab51-4836-f488-046a-cda6bf494859/displayicon.png": "Viper",
    "https://titles.trackercdn.com/valorant-api/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png": "Breach",
    "https://titles.trackercdn.com/valorant-api/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png": "Cypher",
    "https://titles.trackercdn.com/valorant-api/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/displayicon.png": "Sova",
    "https://titles.trackercdn.com/valorant-api/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png": "Omen",
    "https://titles.trackercdn.com/valorant-api/agents/a3bfb853-43b2-7238-a4f1-ad90e9e46bcc/displayicon.png": "Reyna",
    "https://titles.trackercdn.com/valorant-api/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png": "Killjoy"
}

driver = webdriver.Chrome(
    "C:/Users/schoo/Downloads/chromedriver_win32/chromedriver.exe")
driver.set_window_size(1920, 1480)

with open("./scrape.json", mode="w") as f:
    matches = []
    for url in urls:
        driver.get(url)
        WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.CLASS_NAME, "image"))

        game_info_labels = driver.find_elements(
            By.CLASS_NAME, "trn-match-drawer__header-label")
        game_info = driver.find_elements(
            By.CLASS_NAME, "trn-match-drawer__header-value")

        match = {
            "time": game_info_labels[4].text,
            "map": game_info[0].text,
            "score_a": game_info[1].text,
            "score_b": game_info[3].text,
            "team_a": {},
            "team_b": {}
        }

        rows = driver.find_elements(By.CLASS_NAME, "st-content__item")
        for i, row in enumerate(rows):
            name = row.find_element(By.CLASS_NAME, "trn-ign__username").text
            agent_image = row.find_element(
                By.TAG_NAME, "img").get_attribute("src")
            stats = row.find_elements(By.CLASS_NAME, "value")
            match["team_a" if i < 5 else "team_b"][username_to_name[name] if name in username_to_name.keys() else name] = {
                "agent": image_url_to_agent[agent_image],
                "acs": stats[0].text,
                "kills": stats[1].text,
                "deaths": stats[2].text,
                "assists": stats[3].text,
                # "+/-": stats[4].text,
                "kill_deaths": stats[5].text,
                "kill_assist_survive_traded": stats[6].text,
                "first_kill": stats[7].text,
                "first_deaths": stats[8].text,
                "multi_kills": stats[9].text,
                "econ": stats[10].text
            }
        matches.append(match)
    json.dump(matches, f, indent=2)
    f.close()

driver.close()
