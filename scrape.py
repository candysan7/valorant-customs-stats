import json
import time
import os.path
import urllib.request
from urllib.parse import urlparse
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Starting from 10/11/22
urls = [
    "https://tracker.gg/valorant/match/9026099d-b7ab-4208-bf6d-8427b7c2c062?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/1e31a061-81b9-44b4-b4e9-85ba682d4db1?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/e22f48be-9cfc-4837-ab07-d9260be54d74?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/e878e0c4-cab8-4a69-99e5-b29f18abc703?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/418ce446-f8ea-45c0-98f6-14486358add3?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/8a8ec4e8-849a-4a1b-b0fc-ab1490464dcc?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/1b911cb0-1fb4-4087-9c07-466b9991c8fe?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/bc4f5855-dfbd-4589-905b-4335ca59a130?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/e4a9cf52-8764-455f-81d7-921e8c8270c2?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/d29487f4-d110-41bb-9257-f63258364ac3?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/59ebc14d-3a1c-40d6-9b8d-7233a288bdce?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/94b3fc6b-074f-40e1-a2dc-294d68eaddce?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/387cb7f5-1fe3-4a03-bbba-f95674aa1c10?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/873b74bb-f145-4c2d-a49f-12620f81672a?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/f5d502ba-5679-407a-9a13-22abbd824fea?handle=SusTwins%238734",
    "https://tracker.gg/valorant/match/8ee749de-433b-4964-87dc-c13e9e04e904?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/507ae798-5f65-443d-9583-497f9a881c7f?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/3fd2b076-1388-43be-97c7-3ee8d241e241?handle=tangy%230409",
    "https://tracker.gg/valorant/match/741ba201-156c-4f0b-9629-2011ca71ef10?handle=tangy%230409",
    "https://tracker.gg/valorant/match/cefa9d9c-1a3f-43bb-aa11-c7622f444f60?handle=tangy%230409",
    "https://tracker.gg/valorant/match/49ff121d-24d9-4905-ae72-d58d0950d1a6?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/5855ee79-8347-47ca-ab50-099b9d1b5bc2?handle=tangy%230409",
    "https://tracker.gg/valorant/match/59b8f560-e5ff-4763-b103-0a8a249374ea?handle=tangy%230409",
    "https://tracker.gg/valorant/match/b84af821-c189-4538-99ac-3086cae68583?handle=sun%23LULW",
    "https://tracker.gg/valorant/match/894ecb6a-94ab-4b93-b0e3-c2328d1745de?handle=sun%23LULW",
    "https://tracker.gg/valorant/match/ae45fd0b-e967-4ed3-a8cc-bf35c14e76a2?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/72685740-ed00-4125-af65-47d8af2a40bc?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/6d1465a7-37a3-43c9-a832-bda48012e926?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/3d080224-fb11-4ca6-8365-af39f3e7e34a?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/03b78866-1920-4f2b-a6bc-6da429bc1628?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/f027ef8a-781e-489f-af88-67c08863d19b?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/a294da99-b803-4326-98c2-da9b30c2e8df?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/67bfc918-cf0e-4dec-94bb-05e74be59a09?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/f9fb55cc-b96c-49f3-a02c-9585887bb23f?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/30014bd6-5637-4883-9943-92aba1999ed9?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/0230fd80-2538-4fba-8178-f740af345562?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/03824d2a-6b32-47d3-8d92-41aaac4cdecc?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/731284fb-6e14-40e4-8171-914176f699b2?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/6df1e7ff-d33d-4ea9-abd0-e97f33fa5900?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/046c8909-4212-4fab-9ad6-26f75e25492a?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/8293a75b-c366-43cc-840d-da3cadbcdef2?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/bef040b2-e3b3-42b3-8c6b-bf4af9e5c9d7?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/6c87a77f-488e-4a8a-a0ad-9aa0cd1b808a?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/e8380c75-fe6c-42d6-84f3-78d3f6f88fc4?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/bf09a9fe-8f9f-41b5-bcbb-6b8301ab26d7?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/b5909ed7-9e7f-4317-8d84-b08ba97edfa1?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/1a525de2-118e-45d9-983e-7c29b8e3d014?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/2a5da951-ed3d-4505-a47d-245a1ecd29d8?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/a5cdf99a-dec4-4c70-87bf-dc0614ec9a72?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/c23c3452-b57e-4b19-a8dd-f0d8e75ca083?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/1130fc3a-89c2-4318-9e4d-3d28824d8292?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/b82d43e9-5b05-4c1b-a45e-8b357bb9109a?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/2e0c5bc4-af8a-4044-ba2f-94673f0de9d4?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/c9930cfa-d79b-4da3-a643-d6a7d1f6c83e?handle=aylindsay%230613",
]

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
    "danielscutiegf": "susu",
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
    "https://titles.trackercdn.com/valorant-api/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png": "Killjoy",
}

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_extension(
    "C:/Users/StevenTruong/Documents/Code/selenium/uBlock Origin 1.45.2.0.crx"
)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.set_window_size(1920, 1400)

matches = []
# if os.path.exists("./data.json"):
#     with open("./data.json", mode="r") as f:
#         matches = json.load(f)
#     f.close()


# for match in matches:
#     if match["url"] in urls:
#         urls.remove(match["url"])

for url in urls:
    print(f"Scraping from: {url}")
    while True:
        try:
            api_url = f"https://api.tracker.gg/api/v2/valorant/standard/matches/{urlparse(url).path.split('/')[-1]}"
            driver.get(api_url)
            time.sleep(1.5)

            match_json = json.loads(driver.find_element(By.CSS_SELECTOR, "pre").text)[
                "data"
            ]
            match_json["tracker_url"] = url

            # game_info_labels = driver.find_elements(
            #     By.CLASS_NAME, "trn-match-drawer__header-label"
            # )
            # game_info = driver.find_elements(
            #     By.CLASS_NAME, "trn-match-drawer__header-value"
            # )

            # rows = driver.find_elements(By.CLASS_NAME, "st-content__item")
            # for i, row in enumerate(rows):
            #     name = row.find_element(By.CLASS_NAME, "trn-ign__username").text
            #     agent_image = row.find_element(By.TAG_NAME, "img").get_attribute("src")
            #     stats = row.find_elements(By.CLASS_NAME, "value")
            #     match["team_a" if i < 5 else "team_b"].append(
            #         {
            #             "player_name": username_to_name[name]
            #             if name in username_to_name.keys()
            #             else name,
            #             "agent": image_url_to_agent[agent_image],
            #             "average_combat_score": int(stats[0].text),
            #             "kills": int(stats[1].text),
            #             "deaths": int(stats[2].text),
            #             "assists": int(stats[3].text),
            #             # "+/-": stats[4].text,
            #             "kill_deaths": float(stats[5].text),
            #             "kill_assist_survive_traded": int(stats[6].text[:-1]),
            #             "first_kills": int(stats[7].text),
            #             "first_deaths": int(stats[8].text),
            #             "multi_kills": int(stats[9].text),
            #             "econ": int(stats[10].text),
            #         }
            #     )

            matches.append(match_json)
            break
        except Exception as e:
            print(e)
            continue


print("Saving...")
with open("./scrape.json", mode="w") as f:
    # matches.sort(key=lambda m: datetime.strptime(m["time"], "%m/%d/%y, %I:%M %p"))
    json.dump(matches, f, separators=(",", ":"))
    f.close()
print("Done")

driver.close()
