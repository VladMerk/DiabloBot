import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)


url = "https://d2runewizard.com/api/diablo-clone-progress/all"
params = {"token": "E1pjhPc7fX8OZagTPfiJww"}
headers = {
            "D2R-Contact": "qordes@gmail.com",
            "D2R-Platform": "https://discord.gg/qordes",
            "D2R-Repo": "https://github.com/VladMerk",
        }

progress: dict = {}


async def get_json():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, headers=headers) as r:
            if r.status != 200:
                logger.critical("D2R not connected.")
                return
            return await r.json()

server_sorted_list = [
    'ladderSoftcoreAsia',
    'ladderSoftcoreEurope',
    'ladderSoftcoreAmericas',
    'ladderHardcoreAsia',
    'ladderHardcoreEurope',
    'ladderHardcoreAmericas',
    'nonLadderSoftcoreAsia',
    'nonLadderSoftcoreEurope',
    'nonLadderSoftcoreAmericas',
    'nonLadderHardcoreAsia',
    'nonLadderHardcoreEurope',
    'nonLadderHardcoreAmericas',
]


async def main():
    result: dict = {}
    clones = await get_json()
    for item in sorted(clones['servers'],
                      key=lambda x: server_sorted_list.index(x["server"])):
        result[item['server']] = {}

if __name__ == "__main__":
    asyncio.run(main())
