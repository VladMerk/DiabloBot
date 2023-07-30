import logging

from nextcord.ext import commands

from guilds.models import Settings

logger = logging.getLogger(__name__)


class CollectDataCog(commands.Cog, name='Collect commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.debug("Cog 'Collect Data' is loaded")

    @commands.command(name='collect', help='Collect messages from work channel')
    @commands.has_role("Администратор")
    async def collect(self, ctx, limit=None):

        guild_id = await Settings.objects.afirst()
        guild = self.bot.get_guild(guild_id.id)

        channel = guild.system_channel

        messages = await channel.history(limit=limit, oldest_first=True).flatten()

        for message in messages:
            logger.debug(f"Message: {message.author} - {message.content[:10]} - {message.created_at.strftime('%Y-%m-%d %H:%M')}")

        await ctx.send('Сообщения собраны.')

    @commands.command(name='ping', help='Test command of bot')
    async def ping(self, ctx):
        logger.debug('Message !ping')
        await ctx.send('Pong!')


def setup(bot):
    bot.add_cog(CollectDataCog(bot))
