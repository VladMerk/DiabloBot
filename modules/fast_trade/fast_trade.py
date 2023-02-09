from datetime import datetime
import nextcord
from nextcord.ext import commands, tasks
from nextcord.utils import get
from modules.configs.config import fast_trade_discord_channel, server_id, fast_trade_role
from modules.loggers import logger

class FastTrade(commands.Cog, name='Fast Trade Channel'):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.time_to_delete_message = 20
        self.fast_trade_messages.start()

    @tasks.loop(seconds=60)
    async def fast_trade_messages(self):
        channel = self.bot.get_channel(fast_trade_discord_channel)

        if messages := [message async for message in channel.history()]:
            for message in messages:
                if int(message.created_at.timestamp())  + self.time_to_delete_message * 60 <= datetime.now().timestamp() and \
                    not message.pinned:
                    await message.delete()

    @fast_trade_messages.before_loop
    async def befor_fast_trade(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(FastTrade(bot=bot))
