# Keys in output JSON
TEAMMATE_NAME = "teammate_name"
OPPONENT_NAME = "opponent_name"
WINRATE = "winrate"
WINS = "wins"
GAMES = "games"

# Player names
ANDY = "andy"
BRANDON = "brandon"
BRIAN = "brian"
CADE = "cade"
DARWIN = "darwin"
JOSH = "josh"
LINDSEY = "lindsey"
SEQUENTIAL = "sequential"
SOPHIE = "sophie"
STEVE = "steve"
STEVEN = "steven"
SUN = "sun"
SUSI = "susi"
SUSU = "susu"
TANG = "tang"
YANG = "yang"

# Player personal info
player_info = {
    ANDY: {
        "name": "Andy",
        "valorant_tag": "Candysan",
        "discord_pic": "https://i.ibb.co/x5xzfYQ/disc-pic-andy-circle-250-v2.png",
    },
    BRANDON: {
        "name": "Brandon",
        "valorant_tag": "BigBoiB",
        "discord_pic": "TODO",
    },
    BRIAN: {
        "name": "Brian",
        "valorant_tag": "brianwoohoo",
        "discord_pic": "TODO",
    },
    CADE: {
        "name": "Cade",
        "valorant_tag": "RhythmKing",
        "discord_pic": "https://i.ibb.co/c2S6nRZ/disc-pic-cade-circle-250.png",
    },
    DARWIN: {
        "name": "Darwin",
        "valorant_tag": "ChzGorditaCrunch",
        "discord_pic": "https://i.ibb.co/jVR2542/disc-pic-darwin-circle-250.png",
    },
    JOSH: {
        "name": "Josh",
        "valorant_tag": "Bot001341",
        "discord_pic": "https://i.ibb.co/nR7WYQV/disc-pic-josh-circle-250.png",
    },
    LINDSEY: {
        "name": "Lindsey",
        "valorant_tag": "aylindsay",
        "discord_pic": "https://i.ibb.co/kMZxKMy/disc-pic-lindsey-circle.png",
    },
    SEQUENTIAL: {
        "name": "Sequential",
        "valorant_tag": "sequential",
        "discord_pic": "TODO",
    },
    SOPHIE: {
        "name": "Sophie",
        "valorant_tag": "chushberry",
        "discord_pic": "TODO",
    },
    STEVE: {
        "name": "Steve",
        "valorant_tag": "Selintt",
        "discord_pic": "TODO",
    },
    STEVEN: {
        "name": "Steven",
        "valorant_tag": "youngsmasher",
        "discord_pic": "TODO",
    },
    SUN: {
        "name": "Sun",
        "valorant_tag": "sun",
        "discord_pic": "TODO",
    },
    SUSI: {
        "name": "Susi",
        "valorant_tag": "SusTwins",
        "discord_pic": "TODO",
    },
    SUSU: {
        "name": "Susu",
        "valorant_tag": "danielscutiegf",
        "discord_pic": "TODO",
    },
    TANG: {
        "name": "Tang",
        "valorant_tag": "tangy",
        "discord_pic": "TODO",
    },
    YANG: {
        "name": "Yang",
        "valorant_tag": "Tyblerone",
        "discord_pic": "TODO",
    },
}

# Agent names
HARBOR = "Harbor"
FADE = "Fade"
NEON = "Neon"
CHAMBER = "Chamber"
SKYE = "Skye"
YORU = "Yoru"
ASTRA = "Astra"
KAYO = "KAY/O"
PHOENIX = "Phoenix"
RAZE = "Raze"
BRIMSTONE = "Brimstone"
JETT = "Jett"
SAGE = "Sage"
VIPER = "Viper"
BREACH = "Breach"
CYPHER = "Cypher"
SOVA = "Sova"
OMEN = "Omen"
REYNA = "Reyna"
KILLJOY = "Killjoy"

agent_names = sorted(
    [
        HARBOR,
        FADE,
        NEON,
        CHAMBER,
        SKYE,
        YORU,
        ASTRA,
        KAYO,
        PHOENIX,
        RAZE,
        BRIMSTONE,
        JETT,
        SAGE,
        VIPER,
        BREACH,
        CYPHER,
        SOVA,
        OMEN,
        REYNA,
        KILLJOY,
    ]
)

agent_name_to_full_body_image_url = {
    PHOENIX: {"url": "https://i.ibb.co/jr62DmS/agent-phoenix.png"},
    OMEN: {"url": "https://i.ibb.co/gyF9RPn/agent-omen.png"},
    SAGE: {"url": "https://i.ibb.co/3Bjc4Ff/agent-sage.png"},
    HARBOR: {"url": "https://i.ibb.co/cQWBVhF/agent-harbor.png"},
    CYPHER: {"url": "https://i.ibb.co/47jc4bW/agent-cypher.png"},
    SKYE: {"url": "https://i.ibb.co/YWDbNSd/agent-skye.png"},
    ASTRA: {"url": "https://i.ibb.co/tpFTDZP/agent-astra.png"},
    REYNA: {"url": "https://i.ibb.co/Q99BLjb/agent-reyna.png"},
    JETT: {"url": "https://i.ibb.co/jV79G9x/agent-jett.png"},
    REYNA: {"url": "https://i.ibb.co/Q99BLjb/agent-reyna.png"},
    SOVA: {"url": "https://i.ibb.co/7nhNYq3/agent-sova.png"},
    RAZE: {"url": "https://i.ibb.co/m84byGB/agent-raze.png"},
    SAGE: {"url": "https://i.ibb.co/3Bjc4Ff/agent-sage.png"},
    BRIMSTONE: {"url": "https://i.ibb.co/RCygQtF/agent-brimstone.png"},
    OMEN: {"url": "https://i.ibb.co/gyF9RPn/agent-omen.png"},
    KILLJOY: {"url": "https://i.ibb.co/sVZBy9y/agent-killjoy.png"},
    KAYO: {"url": "https://i.ibb.co/zGxz9WH/agent-kayo.png"},
    FADE: {"url": "https://i.ibb.co/HpQ9nmj/agent-fade.png"},
    NEON: {"url": "https://i.ibb.co/kX8npRV/agent-neon.png"},
    CHAMBER: {"url": "https://i.ibb.co/wwW5pw9/agent-chamber.png"},
}

# Map names
ASCENT = "Ascent"
BIND = "Bind"
BREEZE = "Breeze"
FRACTURE = "Fracture"
HAVEN = "Haven"
ICEBOX = "Icebox"
PEARL = "Pearl"
SPLIT = "Split"

# Players of interest
player_names = [
    ANDY,
    BRANDON,
    BRIAN,
    CADE,
    DARWIN,
    JOSH,
    LINDSEY,
    SEQUENTIAL,
    SOPHIE,
    STEVE,
    STEVEN,
    SUN,
    SUSI,
    SUSU,
    TANG,
    YANG,
]

# All maps
maps = [
    ASCENT,
    BIND,
    BREEZE,
    FRACTURE,
    HAVEN,
    ICEBOX,
    PEARL,
    SPLIT,
]
