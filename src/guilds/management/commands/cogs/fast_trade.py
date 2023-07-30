import logging
import traceback
from datetime import datetime

import nextcord
from nextcord.ext import commands, tasks

from guilds.models import Settings

logger = logging.getLogger(__name__)


class FastTrade(commands.Cog, name="Fast Trade Channel"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fast_trade_messages.start()
        logger.debug("Cog 'Fast Trade' is loaded.")

    @tasks.loop(seconds=60)
    async def fast_trade_messages(self):
        try:
            await self.process_fast_trade_messages()
        except Exception as e:
            logger.error(f"An error occured in 'fast_trade_messages': {e}\n {traceback.format_exc()}")

    async def process_fast_trade_messages(self):
        self._data = await Settings.objects.afirst()
        if self._data is None:
            logger.warning("Settings is not found in database.")
            return

        channel_id = self._data.fasttrade_channel_id
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            logger.warning("Fast Trade Channel is not found in database")
            return

        if messages := [message async for message in channel.history()]:
            for message in messages:
                if (
                    int(message.created_at.timestamp()) + self._data.fasttrade_channel_time * 60 <= datetime.now().timestamp()
                    and not message.pinned
                ):
                    await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.message.Message):

        if message.channel.id != self._data.fasttrade_channel_id:
            return
        if message.author.bot:
            logger.debug(f"Bot leave message in {message.channel} channel.")
            return

        server = self.bot.get_guild(self._data.id)
        role = nextcord.utils.get(server.roles, id=self._data.fasttrade_channel_role_id)
        for member in server.members:
            if role in member.roles and message.author != member:
                if len(message.attachments):
                    mess = f"{message.author.mention} в канале {message.channel.mention} оставил сообщение:"
                    f"`{message.content}`"
                    for attach in message.attachments:
                        mess += f"{attach.url}\n"
                    try:
                        await member.send(mess)
                    except Exception:
                        logger.warning(f"Can't send message to {member} channel.")
                        logger.warning(f"Message author: {message.author}")
                else:
                    try:
                        await member.send(
                            f"{message.author.mention} в канале {message.channel.mention} оставил сообщение:" f" `{message.content}`"
                        )
                    except Exception:
                        logger.warning(f"Can't send message to {member} channel.")
                        logger.warning(f"Message author: {message.author}")

    @fast_trade_messages.before_loop
    async def befor_fast_trade(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(FastTrade(bot=bot))
