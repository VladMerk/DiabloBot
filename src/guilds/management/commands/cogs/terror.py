import logging
from datetime import datetime

import aiohttp
import nextcord
from django.conf import settings
from django.core.cache import cache
from nextcord.ext import commands, tasks

from guilds.models import Settings, TerrorZones

logger = logging.getLogger(__name__)


class TerrorZoneChannel(commands.Cog, name="Terror Zone"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.params = {"token": settings.TOKEN_D2R}
        self.url = "https://d2runewizard.com/api/terror-zone"
        self.headers = {
            'D2R-Contact': 'qordes@gmail.com',
            'D2R-Platform': 'https://discord.gg/qordes',
            'D2R-Repo': 'https://github.com/VladMerk'
        }
        self.terror_zone.start()
        logger.debug("Cog 'Terror Zone' is loaded.")

    async def get_json(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url, params=self.params, headers=self.headers) as r:
                if r.status == 200:
                    rjson = await r.json()
                    logger.info(f"New zone is {rjson['terrorZone']['zone']}")
                    return rjson["terrorZone"]["zone"]
                else:
                    logger.warning("Connection error in terror zone function")
                    return None

    async def _get_max_time(self):
        data = await Settings.objects.afirst()
        if data is None:
            logger.warning("Max time is not find in database.")
            return None
        return data.max_time

    @tasks.loop(seconds=30)
    async def terror_zone(self):
        _time = await self._get_max_time()
        if _time is None:
            logger.warning("Max time not found.")
            return

        if datetime.now().minute not in range(2, _time):
            return

        zone = await self.get_json()
        if not zone:
            logger.warning(f"Zone is {zone}. Return from function")
            return

        if not await self.bot.check_redis():
            logger.critical("Redis is not connected!.")
            return

        if cache.get("zone") is None or zone != cache.get("zone"):
            _data = await Settings.objects.afirst()

            server_id = _data.id
            server = self.bot.get_guild(server_id)

            _zone = await TerrorZones.objects.select_related().filter(key=zone).afirst()
            logger.debug(f"{_zone}")
            if _zone is not None:
                message = f"\n**Terror Zone**: {_zone.name_en} in **{_zone.act} Act**\n"
                message += f"**Зона Ужаса**: {_zone.name_ru} в **{_zone.act} акте**\n"
                message += f"\n**Иммунитеты**: {_zone.immunities_en}\n"
                message += f"**Количество пачек с уникальными мобами**: {_zone.boss_packs}\n"
                message += f"**Uniques**: {_zone.super_uniques}\n"
                message += f"**Количество особых сундуков**: {_zone.sparkly_chests}" if bool(_zone.sparkly_chests) else ""
                message += "\nProvided By <https://d2runewizard.com>"
                if _zone.role_id:
                    zone_role = nextcord.utils.get(server.roles, id=_zone.role_id)
                    message += f"\n\n{zone_role.mention}"

                channel = self.bot.get_channel(_data.terror_channel_id)

                await channel.send(message)
                cache.set("zone", zone)

    @terror_zone.before_loop
    async def befor_terror_zone(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(TerrorZoneChannel(bot=bot))
