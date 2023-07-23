import logging
import nextcord

from nextcord.ext import commands
from asgiref.sync import sync_to_async

from guilds.models import Channels

logger = logging.getLogger(__name__)


class ManageChannels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        logger.debug("Cog 'ManageChannels' is loaded.")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: nextcord.abc.GuildChannel):
        _channel = Channels(id=channel.id,
                            name=channel.name)

        await sync_to_async(_channel.save)()
        logger.debug(f"Channel {channel.name} is created in database")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: nextcord.abc.GuildChannel):
        try:
            _channel = await Channels.objects.aget(id=channel.id,
                                        name=channel.name)
        except Exception as e:
            logger.warning(f"Channel {channel.name} not found in database")
            return

        await sync_to_async(_channel.delete)()
        logger.debug(f"Channel {channel.name} is deleted from database")

    @commands.Cog.listener()
    async def on_guild_channel_update(self,
                                      old_channel: nextcord.abc.GuildChannel,
                                      new_channel: nextcord.abc.GuildChannel):
        try:
            _channel = await Channels.objects.aget(id=old_channel.id,
                                                   name=old_channel.name)
        except Exception as e:
            logger.warning(f"Channel {old_channel.name} not found in database")
            return

        _channel.id = new_channel.id
        _channel.name = new_channel.name

        await sync_to_async(_channel.save)()
        logger.debug(f"Channel {new_channel.name} is updated.")


def setup(bot: commands.Bot):
    bot.add_cog(ManageChannels(bot=bot))
