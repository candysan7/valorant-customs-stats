import json

from dateutil.parser import isoparse

from constants import *

player_tags = {
    "Candysan": ANDY,
    "BigBoiB": BRANDON,
    "Brioche": BREE,
    "brianwoohoo": BRIAN,
    "RhythmKing": CADE,
    "ChzGorditaCrunch": DARWIN,
    "Jeff Probst": DARWIN,
    "Mirabel Madrigal": DARWIN,
    "bot001341": JOSH,
    "aylindsay": LINDSEY,
    "Sequential": SEQUENTIAL,
    "chushberry": SOPHIE,
    "alomeirca": STEVE,
    "Selintt": STEVE,
    "spookslayer1": STEVE,
    "youngsmasher": STEVEN,
    "sun": SUN,
    "SusTwins": SUSI,
    "danielscutiegf": SUSU,
    "tangy": TANG,
    "Tyblerone": YANG,
}

# Account identifiers from VALORANT; used for player locations
player_ids = {
    "KOim9KyXvSPhXO6eRFhe_sdVWQ-J6rdj8QAsfqudhJiYMNcNbfkkhlf5cBhLanULZ_J09lsQVYHebA": ANDY,
    "RujpEbc0IH314j9VAhPjv0pEBI3OU1q5jPlWMRruJGpkeIrt6rk1ZjyklEnNCzaIIhNfxybDmTPS6g": BRANDON,
    "zVBj-5l3XxSjxwtH-NLvgj-KCcjCNnU8ePJzG1XMn7GbX9D_Z8qUh8wjITvhm69_X0Oa--XluO_vYQ": BREE,
    "RReD4zGGEQBPZ01t7etkv8VDpaca8kmLMqR9X4t2htNfxLciKXzQUNKc4FBlA5h2a35_65kT6DdIRA": BRIAN,
    "Bm4jdT7LyDkfAamnd3Pxfr79kkrgW-PDXyYhjnCKlHNhqzBSYa3ObumWCjxk07i9Jm1VA-ogVY86QQ": CADE,
    "x4VQ1y3s1A4GOSoFjHnYrOuRKUW2nM5B7Lyy-L_1hPEFj-_Wde6ZYN4f2_4uz9t5Ga7XkWZpzZ4Tfw": DARWIN,
    "C_tY6a_w5RZM-Q4-o4lXmYWyHwR47CdIhc6RqdojrFvYP4__H6fTcEsl9NyeERHG5GhU77fjdPVvaQ": JOSH,
    "HdmC1fwo6fs0IR5aF8YPr_d8Y9O4mGvLEte-ZobPyIIGY_rgprMUsKVcU1bgNGrO64cY0mVe3wLyIA": LINDSEY,
    "cc0hfNaF5_tny7jaSf8N7Bar87EQJt3fLsy85NKGFHBjixtmXfwYgZ9iaIqfaHSwyDvb6HbzOCCuCQ": SEQUENTIAL,
    "QUesI_kn1ehLlxurIHZtD9Ww-9qESBRQ_RodxkG7q_jWaVB5p7eh1VxnKUiuRmW_ABu8l2Elqr7MtQ": SOPHIE,
    "g5ab9-AFyFHyaAzvd2E3YDPxyd_o7XMBQ3oMJEKvVcoCdD5DSWijihWgt4lO3RdeQ6glRVQVQZowTQ": STEVE,
    "9AEt5kjyF3Ho7ZiXaaZA03mCw8_CCF4dP6J8QExrVssTB_5HDXaDhrsgwPzs_Y0o3QVxmN2iqoVpyA": STEVE,
    "ocm6y5CVE3L4l1dIcYoyKzZombwCuVx3vP7pqFe79wCdk_oCAUcaJ0mf7MGwK2lGMx4kt9xirfEq6Q": STEVEN,
    "Ef0d2--EnEXjUkAjOCdoG8l-I6xhsTiwBYfO_hGiNc1ageb7ojel5_ih2GbI68EijY3i_wxgL0_E_A": SUN,
    "QkVviF0Z7UsFptwr0fg-KEMlgbeL7Wg-WpcISvEKUc7CGkBrCt9e1t82Ma7wFwc_CL2Oi0R6Gn0-Fg": SUSI,
    "0JBuaLG15FiA7fEkE3ps24-anUziLtNoowIDmEV7ZBH5wu8gwojY3LKKYtAbKJM90UJY9Tmg7OhLwQ": SUSU,
    "LISiqRtWZpeNmJqirqfyBDFfgTMUNHFz-TuTmNqCGZ4OZSnHcx20SnJc1mDG28w40LHbkCO6ftm3YA": TANG,
    "fxBAnDFK0NgQ00iLw-G2hML2r4E3HAV11OIb-DTCMm77OHfSPogllCktnjup6AglEp2RrNNcgzWdYQ": YANG,
}


def username_to_name(username):
    return player_tags.get(username, username)


def puuid_to_name(puuid):
    return player_ids.get(puuid, puuid)


def process_scrape():
    matches = []
    with open("./scrape.json", mode="r") as f:
        all_match_json = json.load(f)

        for match_json in all_match_json:
            match = {
                "time": match_json["metadata"]["dateStarted"],
                "url": match_json["tracker_url"],
                "map": match_json["metadata"]["mapName"],
                "score_red": None,
                "score_blue": None,
                "team_red": [],
                "team_blue": [],
                "rounds": [
                    {
                        "winning_team": "",
                        "winning_side": "",
                        "win_method": "",
                        "duration": None,
                        "player_stats": [],
                        "damage_events": [],
                        "kills": [],
                    }
                    for _ in range(match_json["metadata"]["rounds"])
                ],
            }

            for segment in match_json["segments"]:
                match segment["type"]:
                    case "round-summary":
                        round_index = segment["attributes"]["round"] - 1
                        match["rounds"][round_index]["winning_team"] = segment["stats"][
                            "winningTeam"
                        ]["value"].lower()
                        match["rounds"][round_index]["win_method"] = segment["stats"][
                            "roundResult"
                        ]["value"].lower()

                    case "player-round":
                        round_index = segment["attributes"]["round"] - 1
                        player_name = username_to_name(
                            segment["attributes"]["platformUserIdentifier"].split("#")[
                                0
                            ]
                        )
                        match["rounds"][round_index]["player_stats"].append(
                            {
                                "player_name": player_name,
                                "team": segment["metadata"]["teamId"].lower(),
                                "side": segment["metadata"]["teamSide"] + "s",
                                "score": segment["stats"]["score"]["value"],
                                "kills": segment["stats"]["kills"]["value"],
                                "deaths": segment["stats"]["deaths"]["value"],
                                "assists": segment["stats"]["assists"]["value"],
                                "damage": segment["stats"]["damage"]["value"],
                                "loadout_value": segment["stats"]["loadoutValue"][
                                    "value"
                                ],
                                "remaining_credits": segment["stats"][
                                    "remainingCredits"
                                ]["value"],
                                "spent_credits": segment["stats"]["spentCredits"][
                                    "value"
                                ],
                            }
                        )

                    case "player-round-damage":
                        round_index = segment["attributes"]["round"] - 1
                        giver_name = username_to_name(
                            segment["attributes"]["platformUserIdentifier"].split("#")[
                                0
                            ]
                        )
                        receiver_name = username_to_name(
                            segment["attributes"][
                                "opponentPlatformUserIdentifier"
                            ].split("#")[0]
                        )
                        match["rounds"][round_index]["damage_events"].append(
                            {
                                "giver_name": giver_name,
                                "receiver_name": receiver_name,
                                "damage": segment["stats"]["damage"]["value"],
                                "legshots": segment["stats"]["legshots"]["value"],
                                "bodyshots": segment["stats"]["bodyshots"]["value"],
                                "headshots": segment["stats"]["headshots"]["value"],
                            }
                        )

                    case "player-round-kills":
                        round_index = segment["attributes"]["round"] - 1
                        killer_name = username_to_name(
                            segment["attributes"]["platformUserIdentifier"].split("#")[
                                0
                            ]
                        )
                        victim_name = username_to_name(
                            segment["attributes"][
                                "opponentPlatformUserIdentifier"
                            ].split("#")[0]
                        )

                        match segment["metadata"]["finishingDamage"]["damageType"]:
                            case "Melee":
                                weapon = "Melee"
                            case "Bomb":
                                weapon = "Bomb"
                            case "Weapon":
                                weapon = segment["metadata"]["weaponName"]
                            case other:
                                # Ability
                                weapon = segment["metadata"]["finishingDamage"][
                                    "damageItem"
                                ]

                        player_locations = list(
                            map(
                                lambda d: {
                                    "player_name": puuid_to_name(d["puuid"]),
                                    "angle": d["viewRadians"],
                                    "location": {
                                        "x": d["location"]["x"],
                                        "y": d["location"]["y"],
                                    },
                                },
                                segment["metadata"]["playerLocations"],
                            ),
                        )

                        killer_location = None
                        for d in player_locations:
                            if d["player_name"] == killer_name:
                                killer_location = d

                        match["rounds"][round_index]["kills"].append(
                            {
                                "killer_name": killer_name,
                                "victim_name": victim_name,
                                "assistants": list(
                                    map(
                                        lambda d: username_to_name(
                                            d["platformUserIdentifier"].split("#")[0]
                                        ),
                                        segment["metadata"]["assistants"],
                                    )
                                ),
                                "killer_location": killer_location,
                                "victim_location": {
                                    "x": segment["metadata"]["opponentLocation"]["x"],
                                    "y": segment["metadata"]["opponentLocation"]["y"],
                                },
                                "player_locations": player_locations,
                                "weapon_name": weapon,
                                "game_time": segment["metadata"]["gameTime"],
                                "round_time": segment["metadata"]["roundTime"],
                                "damage": segment["stats"]["damage"]["value"],
                            }
                        )

                    case "player-summary":
                        player_name = username_to_name(
                            segment["attributes"]["platformUserIdentifier"].split("#")[
                                0
                            ]
                        )
                        match[f"team_{segment['metadata']['teamId'].lower()}"].append(
                            {
                                "player_name": player_name,
                                "agent": segment["metadata"]["agentName"],
                                "average_combat_score": round(
                                    segment["stats"]["scorePerRound"]["value"]
                                ),
                                "kills": segment["stats"]["kills"]["value"],
                                "deaths": segment["stats"]["deaths"]["value"],
                                "assists": segment["stats"]["assists"]["value"],
                                "kill_deaths": round(
                                    segment["stats"]["kdRatio"]["value"]
                                ),
                                "kill_assist_survive_traded": round(
                                    segment["stats"]["kast"]["value"]
                                ),
                                "plants": segment["stats"]["plants"]["value"],
                                "defuses": segment["stats"]["defuses"]["value"],
                                "first_kills": segment["stats"]["firstKills"]["value"],
                                "first_deaths": segment["stats"]["firstDeaths"][
                                    "value"
                                ],
                                "multi_kills": segment["stats"]["multiKills"]["value"],
                                "headshot_accuracy": round(
                                    segment["stats"]["hsAccuracy"]["value"]
                                ),
                                "econ": segment["stats"]["econRating"]["value"],
                            }
                        )

                    case "team-summary":
                        if segment["attributes"]["teamId"] == "Red":
                            match["score_red"] = segment["stats"]["roundsWon"]["value"]
                        else:
                            match["score_blue"] = segment["stats"]["roundsWon"]["value"]

                    case "player-loadout":
                        # Stats on how players performed on pistol/eco/force/full buy rounds
                        pass
                    case other:
                        print(f"Missed type: {segment['type']}")

            for i in range(len(match["rounds"])):
                match["rounds"][i]["kills"].sort(key=lambda x: x["round_time"])
                if (
                    match["rounds"][i]["player_stats"][0]["team"]
                    == match["rounds"][i]["winning_team"]
                ):
                    match["rounds"][i]["winning_side"] = match["rounds"][i][
                        "player_stats"
                    ][0]["side"]
                else:
                    match["rounds"][i]["winning_side"] = (
                        "attackers"
                        if match["rounds"][i]["player_stats"][0]["side"] == "defenders"
                        else "defenders"
                    )

                # Some surrender rounds are marked as elimination
                # Not the most robust method, but no-kill rounds are extremely rare
                if len(match["rounds"][i]["kills"]) == 0:
                    match["rounds"][i]["win_method"] = "surrendered"
                    match["rounds"][i]["duration"] = 0
                    continue

                round_start = (
                    match["rounds"][i]["kills"][0]["game_time"]
                    - match["rounds"][i]["kills"][0]["round_time"]
                )

                if (
                    i < len(match["rounds"]) - 1
                    and len(match["rounds"][i + 1]["kills"]) > 0
                ):
                    # round end = (next round first kill round time) - (next round first kill game time) - (buy phase)
                    round_end = (
                        match["rounds"][i + 1]["kills"][0]["game_time"]
                        - match["rounds"][i + 1]["kills"][0]["round_time"]
                        - 1000
                        * (30 if i + 1 != 12 else 45)  # Round 13 has a longer buy phase
                    )
                else:
                    # round end is just the end of the match for the last round or rounds before surrenders
                    round_end = match_json["metadata"]["duration"]

                match["rounds"][i]["duration"] = round_end - round_start

            matches.append(match)
        f.close()

    with open("./data.json", mode="w") as f:
        matches.sort(key=lambda m: isoparse(m["time"]))
        json.dump(matches, f, indent=2)
        f.close()


if __name__ == "__main__":
    process_scrape()
