import logging
import nextcord

from asgiref.sync import sync_to_async
from nextcord.ext import commands

from guilds.models import Roles

logger = logging.getLogger(__name__)


class ManageRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        logger.debug("Cog 'ManageRoles' is loaded")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: nextcord.Role):
        _role = Roles(id=role.id, name=role.name)

        await sync_to_async(_role.save)()
        logger.debug(f"Role {role.name} is created.")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: nextcord.Role):
        try:
            _role = await Roles.objects.aget(id=role.id, name=role.name)
        except Exception as e:
            logger.warning(f"Role not found.\n{e}")
            return

        await sync_to_async(_role.delete)()
        logger.debug(f"Role {role.name} is deleted.")

    @commands.Cog.listener()
    async def on_guild_role_update(self, old_role: nextcord.Role, new_role: nextcord.Role):
        try:
            _role = await Roles.objects.aget(id=old_role.id, name=old_role.name)
        except Exception as e:
            logger.warning(f"Role not found.\n{e}")
            return

        _role.id = new_role.id
        _role.name = new_role.name

        await sync_to_async(_role.save)()
        logger.debug(f"Role {new_role.name} is updated.")


def setup(bot: commands.Bot):
    bot.add_cog(ManageRoles(bot=bot))
