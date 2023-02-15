import logging
from datetime import datetime

import aiohttp
import nextcord
import redis
from django.conf import settings
from django.core.cache import cache
from guilds.models import Guild, TerrorZones, TerrorZoneTemplate
from nextcord.ext import commands, tasks

logger = logging.getLogger(__name__)


class TerrorZoneChannel(commands.Cog, name='Terror Zone'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.params = {'token': settings.TOKEN_D2R}
        self.url = 'https://d2runewizard.com/api/terror-zone'
        self.terror_zone.start()
        logger.debug("Cog 'Terror Zone' is loaded.")

    async def get_json(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url, params=self.params) as r:
                if r.status == 200:
                    rjson = await r.json()
                    return rjson['terrorZone']['zone']
                else:
                    logger.warning("Connection error in terror zone function")
                    return None

    def check_redis(self):
        try:
            # FIXME Определить настройку адреса сервера в settings.py
            r = redis.Redis(host='127.0.0.1', port=6379)
            return r.ping()
        except redis.exceptions.ConnectionError:
            return False

    @tasks.loop(seconds=30)
    async def terror_zone(self):
        if datetime.now().minute not in range(2, 6):
            return

        zone = await self.get_json()
        if not zone:
            logger.warning(f"Zone is {zone}. Return from function")
            return

        if not self.check_redis():
            logger.critical("Redis is not connected!.")
            return

        logger.debug(f"Zone from site is {zone}. Zone from cache is {cache.get('zone')}")

        if cache.get('zone') is None or zone != cache.get('zone'):
            bzone = await TerrorZoneTemplate.objects.filter(key=zone).afirst()
            if bzone is None:
                logger.warning("New zone not found in database.")
                return
            for guild in self.bot.guilds:
                _zone = await TerrorZones.objects.select_related().filter(zone__key=zone, guild=guild.id).afirst()
                logger.debug(f"{_zone}")
                if _zone is not None:
                    message = f"\n**Terror Zone**: {_zone.zone.name_en} in **{_zone.zone.act} Act**\n"
                    message += f"**Зона Ужаса**: {_zone.zone.name_ru} в **{_zone.zone.act} акте**\n"
                    message += f"\n**Иммунитеты**: {_zone.zone.immunities_en}\n"
                    message += f"**Количество пачек с уникальными мобами**: {_zone.zone.boss_packs}\n"
                    message += f"**Uniques**: {_zone.zone.super_uniques}\n"
                    message += f"**Количество особых сундуков**: {_zone.zone.sparkly_chests}" if bool(_zone.zone.sparkly_chests) else ''
                    message += "\nProvided By <https://d2runewizard.com>"
                    if _zone.role_id:
                        zone_role = nextcord.utils.get(guild.roles, id=_zone.role_id)
                        message += f"\n\n{zone_role.mention}"

                    _guild = await Guild.objects.filter(id=guild.id).afirst()
                    channel = self.bot.get_channel(_guild.terror_channels_id)

                    await channel.send(message)
            cache.set('zone', zone, 60*60)

    @terror_zone.before_loop
    async def befor_terror_zone(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(TerrorZoneChannel(bot=bot))
