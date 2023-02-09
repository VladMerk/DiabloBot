from datetime import datetime
import json
import aiohttp
import nextcord
from nextcord.ext import commands, tasks
from modules.configs.config import token_d2r, terror_zone_discord_channel, server_id
from modules.loggers import logger


class TerrorZone(commands.Cog, name='Terror Zone'):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.params = {'token': token_d2r}
        self.url = 'https://d2runewizard.com/api/terror-zone'
        self.terror_dict = ''
        self.terror = ''
        self.terror_zone.start()

    async def get_json(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url, params=self.params) as r:
                rjson = await r.json()
                self.terror_dict = rjson['terrorZone']['zone']


    def read_json(self, key) -> dict:
        zone = {}
        with open('zone.json') as file:
            zone = json.load(file)
        return zone[key]

    @tasks.loop(seconds=30)
    async def terror_zone(self):
        channel = self.bot.get_channel(terror_zone_discord_channel)
        server = self.bot.get_guild(server_id)

        if datetime.now().minute in range(2, 5):
            await self.get_json()
            if self.terror_dict != '' and self.terror != self.terror_dict or self.terror == '':

                self.terror = self.terror_dict
                zone_json = self.read_json(self.terror)

                message = f"\n**Terror Zone**: {zone_json['name']['en']} in **{zone_json['act']} Act**\n"
                message += f"**Зона Ужаса**: {zone_json['name']['ru']} в **{zone_json['act']} акте**\n"
                message += f"\n**Иммунитеты**: {zone_json['immunities']['ru']}\n"
                message += f"**Количество пачек с уникальными мобами**: {zone_json['boss_packs']}\n"
                message += f"**Uniques**: {zone_json['super_uniques']}\n"
                message += f"**Количество особых сундуков**: {zone_json['sparkly_chests']}" if zone_json['sparkly_chests'] > 0 else ''
                message += "\nProvided By <https://d2runewizard.com>"
                try:
                    role = nextcord.utils.get(server.roles, name=zone_json['role'])
                    message += f"\n\n{role.mention}"
                except Exception as e:
                    logger.info(f"Error get role {zone_json['role']}")
                    logger.info(f"Error get role_id {zone_json['role_id']}")
                    logger.error(f"Error is {e}")

                await channel.send(message)

    @terror_zone.before_loop
    async def befor_terror_zone(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(TerrorZone(bot=bot))
