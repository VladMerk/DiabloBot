import logging
import traceback
from datetime import datetime

from nextcord.ext import commands, tasks

from guilds.models import Settings

logger = logging.getLogger(__name__)


class FastTrade(commands.Cog, name="Fast Trade Channel"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.time_to_delete_message = 20
        self.fast_trade_messages.start()
        logger.debug("Cog 'Fast Trade' is loaded.")

    @tasks.loop(seconds=60)
    async def fast_trade_messages(self):
        try:
            await self.process_fast_trade_messages()
        except Exception as e:
            logger.error(f"An error occured in 'fast_trade_messages': {e}\n {traceback.format_exc()}")

    async def process_fast_trade_messages(self):
        _data = await Settings.objects.afirst()
        if _data is None:
            logger.warning("ID for fast_trade channel is not found in database.")
            return
        channel_id = _data.fasttrade_channel_id
        channel = self.bot.get_channel(channel_id)

        if messages := [message async for message in channel.history()]:
            for message in messages:
                if (
                    int(message.created_at.timestamp()) + self.time_to_delete_message * 60 <= datetime.now().timestamp()
                    and not message.pinned
                ):
                    await message.delete()

    @fast_trade_messages.before_loop
    async def befor_fast_trade(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(FastTrade(bot=bot))
