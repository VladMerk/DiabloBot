import logging
import nextcord

from nextcord.ext import commands
from asgiref.sync import sync_to_async
from django.utils.timezone import now

from guilds.models import Roles
from users.models import DiscordUser

logger = logging.getLogger(__name__)


class ManageUsers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        logger.debug("Cog 'ManageUsers' is loaded")

    @commands.command(name='update_users', help='Update users of guild')
    @commands.has_any_role("Администратор")
    async def update_users(self, ctx):
        guild_id = self.bot.guilds.pop().id
        guild = self.bot.get_guild(guild_id)

        for member in guild.members:
            try:
                _member = await DiscordUser.objects.aget(id=member.id)
                logger.debug(f"Found member {_member}")
            except Exception as e:
                logger.warning(f"Exception users as {e}")
                continue

            _member.username = member.name

            for role in member.roles:
                try:
                    _role = await Roles.objects.aget(name=role.name)
                except Exception as e:
                    logger.warning(f"Role users exception: \{e}")
                    continue
                await sync_to_async(_member.roles.add)(_role)
                logger.debug(f"Role for {member}::{_role}")

            await sync_to_async(_member.save)()

            logger.debug(f"Member {member.name} is updated.")

        await ctx.send('Данные пользователей обновлены!')

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        """Event когда пользователь подключается к серверу"""
        _member = DiscordUser(id=member.id,
                              username=member.name,
                              discriminator=member.discriminator,
                              bot=member.bot,
                              joined_at=member.joined_at,
                            )
        await sync_to_async(_member.save)()

        for role in member.roles:
            try:
                _role = await Roles.objects.aget(id=role.id)
            except Exception as e:
                logger.warning(f"Role {role.id}#{role.name} not found in database")
                continue
            await sync_to_async(_member.roles.add)(_role)

        await sync_to_async(_member.save)()
        logger.debug(f"Member {member.name} is added to database")

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        """Event когда пользователь уходит с сервера"""
        try:
            _member = await DiscordUser.objects.aget(id=member.id)
        except Exception as e:
            logger.warning(f"User {member.name} with #{member.id} not found: \n{e}")
            return

        _member.removed_at = now()

        await sync_to_async(_member.save)()
        logger.debug(f"Member {member.name} is deleted from database")

    @commands.Cog.listener()
    async def on_member_update(self, old: nextcord.Member, new: nextcord.Member):
        """Event когда пользователь обновляет свои данные в гильдии дискорда.
           Обновляемые данные в этом эвенте:
                - nickname
                - roles
                - pending
        """
        try:
            _member = await DiscordUser.objects.aget(id=old.id)
        except Exception as e:
            logger.warning(f"Member {old.name} with #{old.id} not found in database: \n{e}")
            return

        _member.username = new.name

        await sync_to_async(_member.roles.clear)()

        for role in new.roles:
            try:
                _role = await Roles.objects.aget(id=role.id)
            except Exception as e:
                logger.warning(f"Role {role.id}#{role.name} not found in database")
                continue
            await sync_to_async(_member.roles.add)(_role)

        await sync_to_async(_member.save)()
        logger.debug(f"Member {new.name} with #{new.id} is updated.")

    @commands.Cog.listener()
    async def on_user_update(self, old: nextcord.User, new: nextcord.User):
        """Event когда пользователь обновляет данные профиля дискорда.
           Обновляемые данные при этом:
                - avatar
                - name
                - discriminator
                """
        try:
            _member = await DiscordUser.objects.aget(id=old.id)
        except Exception as e:
            logger.warning(f"User {old.name} with #{old.id} not found in database:\n{e}")
            return

        _member.username = new.name
        _member.discriminator = new.discriminator

        await sync_to_async(_member.save)()
        logger.debug(f"User {new.name}#{new.discriminator} with #{new.id} is updated")


def setup(bot: commands.Bot):
    bot.add_cog(ManageUsers(bot=bot))
