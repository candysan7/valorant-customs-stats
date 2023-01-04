import json

player_tags = {
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


def username_to_name(username):
    return player_tags[username] if username in player_tags else username


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
                    "win_method": "",
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
                    match["rounds"][round_index - 1]["win_method"] = segment["stats"][
                        "roundResult"
                    ]["value"].lower()

                case "player-round":
                    round_index = segment["attributes"]["round"] - 1
                    player_name = username_to_name(
                        segment["attributes"]["platformUserIdentifier"].split("#")[0]
                    )
                    match["rounds"][round_index]["player_stats"].append(
                        {
                            "player_name": player_name,
                            "team": segment["metadata"]["teamId"].lower(),
                            "side": segment["metadata"]["teamSide"],
                            "score": segment["stats"]["score"]["value"],
                            "kills": segment["stats"]["kills"]["value"],
                            "deaths": segment["stats"]["deaths"]["value"],
                            "assists": segment["stats"]["assists"]["value"],
                            "damage": segment["stats"]["damage"]["value"],
                            "loadout_value": segment["stats"]["loadoutValue"]["value"],
                            "remaining_credits": segment["stats"]["remainingCredits"][
                                "value"
                            ],
                            "spent_credits": segment["stats"]["spentCredits"]["value"],
                        }
                    )

                case "player-round-damage":
                    round_index = segment["attributes"]["round"] - 1
                    giver_name = username_to_name(
                        segment["attributes"]["platformUserIdentifier"].split("#")[0]
                    )
                    receiver_name = username_to_name(
                        segment["attributes"]["opponentPlatformUserIdentifier"].split(
                            "#"
                        )[0]
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
                        segment["attributes"]["platformUserIdentifier"].split("#")[0]
                    )
                    victim_name = username_to_name(
                        segment["attributes"]["opponentPlatformUserIdentifier"].split(
                            "#"
                        )[0]
                    )

                    if segment["metadata"]["finishingDamage"]["damageType"] != "Weapon":
                        # E.g., bomb or ability kills
                        weapon = segment["metadata"]["finishingDamage"]["damageItem"]
                    else:
                        weapon = segment["metadata"]["weaponName"]
                    match["rounds"][round_index]["kills"].append(
                        {
                            "killer_name": killer_name,
                            "victim_name": victim_name,
                            "assistants": list(
                                map(
                                    lambda d: d["platformUserIdentifier"].split("#")[0],
                                    segment["metadata"]["assistants"],
                                )
                            ),
                            "weapon_name": weapon,
                            "round_time": segment["metadata"]["roundTime"],
                            "damage": segment["stats"]["damage"]["value"],
                        }
                    )

                case "player-summary":
                    player_name = username_to_name(
                        segment["attributes"]["platformUserIdentifier"].split("#")[0]
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
                            "kill_deaths": round(segment["stats"]["kdRatio"]["value"]),
                            "kill_assist_survive_traded": round(
                                segment["stats"]["kast"]["value"]
                            ),
                            "first_kills": segment["stats"]["firstKills"]["value"],
                            "first_deaths": segment["stats"]["firstDeaths"]["value"],
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

        for round_data in match["rounds"]:
            round_data["kills"].sort(key=lambda x: x["round_time"])
        matches.append(match)
    f.close()

with open("./data.json", mode="w") as f:
    json.dump(matches, f, indent=2)
    f.close()
