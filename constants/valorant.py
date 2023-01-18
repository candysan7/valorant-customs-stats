# Sides
ATTACKERS = "attackers"
DEFENDERS = "defenders"

# Win methods
SURRENDERED = "surrendered"
ELIMINIATION = "elimination"
DEFUSE = "defuse"
DETONATE = "detonate"
TIME = "time"

# Agent names
ASTRA = "Astra"
BREACH = "Breach"
BRIMSTONE = "Brimstone"
CHAMBER = "Chamber"
CYPHER = "Cypher"
FADE = "Fade"
HARBOR = "Harbor"
JETT = "Jett"
KAYO = "KAY/O"
KILLJOY = "Killjoy"
NEON = "Neon"
OMEN = "Omen"
PHOENIX = "Phoenix"
RAZE = "Raze"
REYNA = "Reyna"
SAGE = "Sage"
SKYE = "Skye"
SOVA = "Sova"
VIPER = "Viper"
YORU = "Yoru"

# Roles
CONTROLLER = "Controller"
DUELIST = "Duelist"
INITIATOR = "Initiator"
SENTINEL = "Sentinel"

# Map names
ASCENT = "Ascent"
BIND = "Bind"
BREEZE = "Breeze"
FRACTURE = "Fracture"
HAVEN = "Haven"
ICEBOX = "Icebox"
LOTUS = "Lotus"
PEARL = "Pearl"
SPLIT = "Split"

AGENT_NAMES = [
    ASTRA,
    BREACH,
    BRIMSTONE,
    CHAMBER,
    CYPHER,
    FADE,
    HARBOR,
    JETT,
    KAYO,
    KILLJOY,
    NEON,
    OMEN,
    PHOENIX,
    RAZE,
    REYNA,
    SAGE,
    SKYE,
    SOVA,
    VIPER,
    YORU,
]

ROLE_NAMES = [CONTROLLER, DUELIST, INITIATOR, SENTINEL]

AGENT_NAME_TO_FULL_BODY_IMAGE_URL = {
    ASTRA: "https://i.ibb.co/tpFTDZP/agent-astra.png",
    BREACH: "https://i.ibb.co/GtG7Z01/agent-breach.png",
    BRIMSTONE: "https://i.ibb.co/RCygQtF/agent-brimstone.png",
    CHAMBER: "https://i.ibb.co/wwW5pw9/agent-chamber.png",
    CYPHER: "https://i.ibb.co/47jc4bW/agent-cypher.png",
    FADE: "https://i.ibb.co/HpQ9nmj/agent-fade.png",
    HARBOR: "https://i.ibb.co/cQWBVhF/agent-harbor.png",
    JETT: "https://i.ibb.co/jV79G9x/agent-jett.png",
    KAYO: "https://i.ibb.co/zGxz9WH/agent-kayo.png",
    KILLJOY: "https://i.ibb.co/sVZBy9y/agent-killjoy.png",
    NEON: "https://i.ibb.co/kX8npRV/agent-neon.png",
    OMEN: "https://i.ibb.co/gyF9RPn/agent-omen.png",
    PHOENIX: "https://i.ibb.co/jr62DmS/agent-phoenix.png",
    RAZE: "https://i.ibb.co/m84byGB/agent-raze.png",
    REYNA: "https://i.ibb.co/Q99BLjb/agent-reyna.png",
    SAGE: "https://i.ibb.co/3Bjc4Ff/agent-sage.png",
    SKYE: "https://i.ibb.co/YWDbNSd/agent-skye.png",
    SOVA: "https://i.ibb.co/7nhNYq3/agent-sova.png",
    VIPER: "https://i.ibb.co/Kxd71pz/agent-viper.png",
    YORU: "https://i.ibb.co/fC5Kcq1/agent-yoru.png",
}

AGENT_NAME_TO_ROLE = {
    ASTRA: CONTROLLER,
    BREACH: INITIATOR,
    BRIMSTONE: CONTROLLER,
    CHAMBER: SENTINEL,
    CYPHER: SENTINEL,
    FADE: INITIATOR,
    HARBOR: CONTROLLER,
    JETT: DUELIST,
    KAYO: INITIATOR,
    KILLJOY: SENTINEL,
    NEON: DUELIST,
    OMEN: CONTROLLER,
    PHOENIX: DUELIST,
    RAZE: DUELIST,
    REYNA: DUELIST,
    SAGE: SENTINEL,
    SKYE: INITIATOR,
    SOVA: INITIATOR,
    VIPER: CONTROLLER,
    YORU: DUELIST,
}

# All maps
MAP_NAMES = [
    ASCENT,
    BIND,
    BREEZE,
    FRACTURE,
    HAVEN,
    ICEBOX,
    LOTUS,
    PEARL,
    SPLIT,
]
