import logging
import aiohttp
import nextcord
from django.conf import settings
from django.core.cache import cache
from nextcord.ext import commands, tasks
from guilds.models import Settings

logger = logging.getLogger(__name__)


class Clone(commands.Cog, name="Clone Diablo"):
    def __init__(self, bot: commands.Bot):
        self.top_clone_server = None
        self.bot = bot
        self.url = "https://d2runewizard.com/api/diablo-clone-progress/all"
        self.params = {"token": settings.TOKEN_D2R}
        self.headers = {
            "D2R-Contact": "qordes@gmail.com",
            "D2R-Platform": "https://discord.gg/qordes",
            "D2R-Repo": "https://github.com/VladMerk",
        }
        self.progress: dict[str, list] = {}
        self.flag = 0
        self.region = {1: "America", 2: "Europe", 3: "Asia"}
        self.ladder = {1: "Ladder", 2: "NonLadder"}
        self.hc = {1: "Hardcore", 2: "Softcore"}
        self.clone.start()
        logger.debug("Cog 'Clone Diablo' is loaded")

    async def get_json(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url, params=self.params, headers=self.headers
            ) as r:
                if r.status != 200:
                    logger.critical("D2R not connected.")
                    self.progress = None
                    return
                rjson = await r.json()
                self.progress = {
                    item["server"]: self.parse_server_data(item)
                    for item in rjson["servers"]
                }

    def parse_server_data(self, item):
        return {
            "server": item["server"],
            "progres": item["progress"],
            "ladder": item["ladder"],
            "hardcore": item["hardcore"],
            "region": item["region"],
            "lastUpdate": item["lastUpdate"]["seconds"],
        }

    def get_message(self, prg: dict) -> str:
        message = ""
        if self.flag:
            message += "\nПоследнее изменение:\n"
            message += self.get_server(prg, [prg[self.top_clone_server]["server"]])

        message += "***Ladder***\n"
        message += self.get_server(
            prg,
            ["ladderSoftcoreAsia", "ladderSoftcoreEurope", "ladderSoftcoreAmericas"],
        )
        message += self.get_server(
            prg,
            ["ladderHardcoreAsia", "ladderHardcoreEurope", "ladderHardcoreAmericas"],
        )

        message += "***NonLadder***\n"
        message += self.get_server(
            prg,
            [
                "nonLadderSoftcoreAsia",
                "nonLadderSoftcoreEurope",
                "nonLadderSoftcoreAmericas",
            ],
        )
        message += self.get_server(
            prg,
            [
                "nonLadderHardcoreAsia",
                "nonLadderHardcoreEurope",
                "nonLadderHardcoreAmericas",
            ],
        )

        message += "\nProvided By <https://d2runewizard.com>"
        return message

    def get_server(self, prg: dict, servers: list) -> str:
        mess = ""
        for server in servers:
            progress = prg[server]["progres"]
            ladder_type = "Ladder" if prg[server]["ladder"] else "NonLadder"
            hardcore_type = "Hardcore" if prg[server]["hardcore"] else "Softcore"
            region = prg[server]["region"]
            last_update = prg[server]["lastUpdate"]
            mess += f"**[{progress}/6]** {ladder_type} {hardcore_type} {region} <t:{last_update}:R>\n"
        return mess + "\n"

    @tasks.loop(seconds=30)
    async def clone(self):
        if not await self.bot.check_redis():
            logger.critical("Redis is not connected!")
            return

        data = await Settings.objects.afirst()
        try:
            channel_id = data.clone_channel_id
        except Exception as e:
            logger.warning(f"Exception: {e}")
            return

        if channel_id is None:
            logger.warning("ID for clone channel not found in database.")
            return

        channel = self.bot.get_channel(channel_id)

        await self.get_json()
        if self.progress is None:
            logger.warning("No data from D2R")
            return

        locale_value = cache.get("clone")

        if locale_value != {} and cache.get("clone") is not None:
            for server in self.progress:
                if locale_value[server]["progres"] != self.progress[server]["progres"]:
                    self.top_clone_server = server
                    self.flag = 1
                    cache.set("clone", self.progress)
                    break
        else:
            cache.set("clone", self.progress)
            await channel.purge()
            await channel.send(self.get_message(self.progress))

        if self.flag:
            await channel.purge()
            await channel.send(self.get_message(self.progress))
            self.flag = 0

    @clone.before_loop
    async def before_clone(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.message.Message):
        data = await Settings.objects.afirst()

        if message.channel.id == data.clone_channel_id:
            try:
                await message.publish()
            except Exception as e:
                logger.warning(f"Не удалось опубликовать сообщение. Причина:\n{e}")
                return
            logger.debug(f"Message in {message.channel} channel is published.")


def setup(bot: commands.Bot):
    bot.add_cog(Clone(bot=bot))
