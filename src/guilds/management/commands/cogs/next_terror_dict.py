import asyncio
import logging

import aiohttp
from django.conf import settings

logger = logging.getLogger(__name__)


TZ_ID_TO_STRING = {
    17: "Burial Grounds</br>Crypt</br>Mausoleum",
    33: "Cathedral</br>Catacombs",
    3: "Cold Plains</br>Cave",
    5: "Darkwood</br>Underground Passage",
    2: "Blood Moor</br>Den of Evil",
    28: "Jail</br>Barracks",
    39: "Moo Moo Farm",
    4: "Stony Field",
    6: "Black Marsh</br>The Hole",
    20: "Forgotten Tower",
    12: "Pit",
    38: "Tristram",
    47: "Lut Gholein Sewers",
    41: "Stony Tomb</br>Rocky Waste",
    42: "Dry Hills</br>Halls of the Dead",
    43: "Far Oasis",
    44: "Lost City</br>Valley of Snakes</br>Claw Viper Temple",
    65: "Ancient Tunnels",
    66: "Tal Rasha's Tombs",
    74: "Arcane Sanctuary",
    76: "Spider Forest</br>Spider Cavern",
    77: "Great Marsh",
    78: "Flayer Jungle and Dungeon",
    80: "Kurast Bazaar</br>Temples",
    83: "Travincal",
    100: "Durance of Hate",
    104: "Outer Steppes</br>Plains of Despair",
    106: "City of the Damned</br>River of Flame",
    108: "Chaos Sanctuary",
    110: "Bloody Foothills</br>Frigid Highlands</br>Abbadon",
    112: "Arreat Plateau</br>Pit of Acheron",
    113: "Crystalline Passage</br>Frozen River",
    121: "Nihlathak's Temple and Halls",
    115: "Glacial Trail</br>Drifter Cavern",
    118: "Ancient's Way</br>Icy Cellar",
    128: "Worldstone Keep</br>Throne of Destruction</br>Worldstone Chamber",
}

TZ_ID_TO_STRING2 = {
    0: "None",
    1: "Rogue Encampment",
    2: "Blood Moor",
    3: "Cold Plains",
    4: "Stony Field",
    5: "Dark Wood",
    6: "Black Marsh",
    7: "Tamoe Highland",
    8: "Den Of Evil",
    9: "Cave Level 1",
    10: "Underground Passage Level 1",
    11: "Hole Level 1",
    12: "Pit Level 1",
    13: "Cave Level 2",
    14: "Underground Passage Level 2",
    15: "Hole Level 2",
    16: "Pit Level 2",
    17: "Burial Grounds",
    18: "Crypt",
    19: "Mausoleum",
    20: "Forgotten Tower",
    21: "Tower Cellar Level 1",
    22: "Tower Cellar Level 2",
    23: "Tower Cellar Level 3",
    24: "Tower Cellar Level 4",
    25: "Tower Cellar Level 5",
    26: "Monastery Gate",
    27: "Outer Cloister",
    28: "Barracks",
    29: "Jail Level 1",
    30: "Jail Level 2",
    31: "Jail Level 3",
    32: "Inner Cloister",
    33: "Cathedral",
    34: "Catacombs Level 1",
    35: "Catacombs Level 2",
    36: "Catacombs Level 3",
    37: "Catacombs Level 4",
    38: "Tristram",
    39: "Moo Moo Farm",
    40: "Lut Gholein",
    41: "Rocky Waste",
    42: "Dry Hills",
    43: "Far Oasis",
    44: "Lost City",
    45: "Valley Of Snakes",
    46: "Canyon Of The Magi",
    47: "A2 Sewers Level 1",
    48: "A2 Sewers Level 2",
    49: "A2 Sewers Level 3",
    50: "Harem Level 1",
    51: "Harem Level 2",
    52: "Palace Cellar Level 1",
    53: "Palace Cellar Level 2",
    54: "Palace Cellar Level 3",
    55: "Stony Tomb Level 1",
    56: "Halls Of The Dead Level 1",
    57: "Halls Of The Dead Level 2",
    58: "Claw Viper Temple Level 1",
    59: "Stony Tomb Level 2",
    60: "Halls Of The Dead Level 3",
    61: "Claw Viper Temple Level 2",
    62: "Maggot Lair Level 1",
    63: "Maggot Lair Level 2",
    64: "Maggot Lair Level 3",
    65: "Ancient Tunnels",
    66: "Tal Rashas Tomb #1",
    67: "Tal Rashas Tomb #2",
    68: "Tal Rashas Tomb #3",
    69: "Tal Rashas Tomb #4",
    70: "Tal Rashas Tomb #5",
    71: "Tal Rashas Tomb #6",
    72: "Tal Rashas Tomb #7",
    73: "Duriels Lair",
    74: "Arcane Sanctuary",
    75: "Kurast Docktown",
    76: "Spider Forest",
    77: "Great Marsh",
    78: "Flayer Jungle",
    79: "Lower Kurast",
    80: "Kurast Bazaar",
    81: "Upper Kurast",
    82: "Kurast Causeway",
    83: "Travincal",
    84: "Spider Cave",
    85: "Spider Cavern",
    86: "Swampy Pit Level 1",
    87: "Swampy Pit Level 2",
    88: "Flayer Dungeon Level 1",
    89: "Flayer Dungeon Level 2",
    90: "Swampy Pit Level 3",
    91: "Flayer Dungeon Level 3",
    92: "A3 Sewers Level 1",
    93: "A3 Sewers Level 2",
    94: "Ruined Temple",
    95: "Disused Fane",
    96: "Forgotten Reliquary",
    97: "Forgotten Temple",
    98: "Ruined Fane",
    99: "Disused Reliquary",
    100: "Durance Of Hate Level 1",
    101: "Durance Of Hate Level 2",
    102: "Durance Of Hate Level 3",
    103: "The Pandemonium Fortress",
    104: "Outer Steppes",
    105: "Plains Of Despair",
    106: "City Of The Damned",
    107: "River Of Flame",
    108: "Chaos Sanctuary",
    109: "Harrogath",
    110: "Bloody Foothills",
    111: "Frigid Highlands",
    112: "Arreat Plateau",
    113: "Crystalized Passage",
    114: "Frozen River",
    115: "Glacial Trail",
    116: "Drifter Cavern",
    117: "Frozen Tundra",
    118: "Ancient's Way",
    119: "Icy Cellar",
    120: "Arreat Summit",
    121: "Nihlathaks Temple",
    122: "Halls Of Anguish",
    123: "Halls Of Pain",
    124: "Halls Of Vaught",
    125: "Abaddon",
    126: "Pit Of Acheron",
    127: "Infernal Pit",
    128: "The Worldstone Keep Level 1",
    129: "The Worldstone Keep Level 2",
    130: "The Worldstone Keep Level 3",
    131: "Throne Of Destruction",
    132: "The Worldstone Chamber",
    133: "Matron's Den",
    134: "Fogotten Sands",
    135: "Furnace of Pain",
    136: "Uber Tristram",
}

next_terror = TZ_ID_TO_STRING | TZ_ID_TO_STRING2

url = "https://www.d2emu.com/api/v1/tz"
headers: dict[str, str] = {
    'x-emu-username': 'qordes',
    'x-emu-token': settings.TOKEN_EMU
}


async def get_next_terror_zone():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as r:
            if r.status == 200:
                rjson = await r.json()
                logger.info(f"Next Terror zone is {rjson}")
                return "\n".join(next_terror[int(zone)] for zone in rjson["next"])
            else:
                logger.warning("Connection error in next terror zone function")
                return None


if __name__ == "__main__":
    asyncio.run(get_next_terror_zone())
