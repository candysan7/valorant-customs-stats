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
    "https://tracker.gg/valorant/match/8f2cbb25-fec7-48e7-b3f7-446bf444080c?handle=aylindsay%230613",
    "https://tracker.gg/valorant/match/7fc820f4-9191-4f92-8121-f33a47c046d3?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/e0e9eba6-c3c9-4963-9fb6-66fb9db1e6af?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/9cc3048f-e28a-4577-b1c9-fa1a3495ee60?handle=Candysan%23NA7",
    "https://tracker.gg/valorant/match/9eba2d2e-a48f-4b24-b1dd-fce1b779449a?handle=Candysan%23NA7",
    "https://tracker.gg/valorant/match/536889a5-d5a2-41d4-be3f-467f81e818ed?handle=Candysan%23NA7",
    "https://tracker.gg/valorant/match/af80e60b-1b96-40f0-9283-a37e58a34468?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/657e3142-f0aa-4b5a-8e7e-e861793efcdf?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/953472e5-4fc4-42dc-a387-99d3839472c2?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/318eae24-0bff-40e7-b819-049770b948b7?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/faa22e0f-af93-4bb7-9f83-c3d6b60cb32c?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/7433d77b-cfb1-4194-99b3-4635e67f4c45?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/ee3039fe-1ee3-4e51-bdb0-bc0219d8cb11?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/b030f339-0329-49a2-98b2-515961726d92?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/ef2dd0ae-4fa8-4d27-8ef7-df99b4bf39b8?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/11b24d94-a872-4e9d-a9fe-4859c5c21189?handle=youngsmasher%23NA1",
    "https://tracker.gg/valorant/match/5d04b37c-2253-48bd-aedc-188483157600?handle=ChzGorditaCrunch%23darw",
    "https://tracker.gg/valorant/match/210d3cbd-ddd3-488e-8c02-e098ecb1c3d0?handle=ChzGorditaCrunch%23darw",
    "https://tracker.gg/valorant/match/ede12260-15ea-4741-a905-c8591ef2d30c?handle=youngsmasher%23NA1",
]

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.set_window_size(852, 480)

matches = []
if os.path.exists("./scrape.json"):
    with open("./scrape.json", mode="r") as f:
        matches = json.load(f)
    f.close()


for match in matches:
    if match["tracker_url"] in urls:
        urls.remove(match["tracker_url"])

for url in urls:
    print(f"Scraping from: {url}")
    while True:
        try:
            api_url = f"https://api.tracker.gg/api/v2/valorant/standard/matches/{urlparse(url).path.split('/')[-1]}"
            driver.get(api_url)
            time.sleep(1)

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
