import nextcord
import logging
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from nextcord.ext import commands
from nextcord.utils import get
from django.conf import settings
from asgiref.sync import sync_to_async

from guilds.models import Channel, Guild, Roles
from users.models import User

logger = logging.getLogger(__name__)

class Client(commands.Bot):

    async def on_ready(self):
        '''
        Функция срабатывает при первом запуске бота
        '''
        for guild in self.guilds:
            # проходим по всем серверам к которым подключен бот
            user, user_created = await sync_to_async(User.objects.get_or_create)(id=guild.owner.id,
                                                                                username=guild.owner.name,
                                                                                discriminator=guild.owner.discriminator)
            if user_created:
                logger.debug(f"User: {user.name} is created")
            _guild, created = await sync_to_async(Guild.objects.get_or_create)(id=guild.id,
                                                                            name=guild.name,
                                                                            owner=user)
            if created:
                logger.info(f"Created guild: {_guild.name}")
            # проходим по всем каналам на сервере и добавляем их в базу, если их нет
            for channel in guild.channels:
                if channel.type != 4:
                    _channel, created = await sync_to_async(Channel.objects.get_or_create)(id=channel.id,
                                                                                        name=channel.name,
                                                                                        guild=_guild)
                if created:
                    logger.info(f"Channel {channel.name} is created.")
            for role in guild.roles:
                _role, created = await sync_to_async(Roles.objects.get_or_create)(id=role.id,
                                                                                    name=role.name,
                                                                                    guild=_guild)
                if created:
                    logger.debug(f"{_role.name}")
            for member in guild.members:
                _member, created = await sync_to_async(User.objects.get_or_create)(id=member.id,
                                                                                    username=member.name,
                                                                                    discriminator=member.discriminator)
                if created:
                    logger.info(f"{_member.username}")

        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")




class Command(BaseCommand):
    help = "Runing bot command"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        client = Client(command_prefix="!", intents=nextcord.Intents.all())
        client.load_extension("guilds.management.commands.cogs.terror")
        client.run(settings.TOKEN)
