import logging

import nextcord
import redis
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from nextcord.ext import commands

from guilds.models import Channels, Roles, Settings
from users.models import DiscordUser

logger = logging.getLogger(__name__)


class Client(commands.Bot):

    async def check_redis(self):
        try:
            r = redis.Redis(host="redis", port=6379)
            return r.ping()
        except redis.exceptions.ConnectionError:
            return False

    async def on_ready(self):
        server = self.guilds.pop()

        _settings, created = await sync_to_async(Settings.objects.get_or_create)(id=server.id, name=server.name)
        if created:
            logger.debug(f"Settings server {server} is created")

        for channel in server.channels:
            if channel.type != 4:   # 4 - группа каналов
                _channel, created = await sync_to_async(Channels.objects.get_or_create)(id=channel.id, name=channel.name)
                if created:
                    logger.debug(f"Added Channel {channel.name} in database")

        for role in server.roles:
            _role, created = await sync_to_async(Roles.objects.get_or_create)(id=role.id, name=role.name)
            if created:
                logger.debug(f"Added role {role.name} in database")

        for member in server.members:
            try:
                _member, created = await sync_to_async(DiscordUser.objects.get_or_create)(id=member.id,
                                                                                      username=member.name,
                                                                                      discriminator=member.discriminator,
                                                                                      bot=member.bot,
                                                                                      joined_at=member.joined_at)
            except IntegrityError as i:
                logger.warning(f"User {member.name} already in database.\n{i}")
            except Exception as e:
                logger.warning(f"Exception in added user {member.name} in database")
            if created:
                logger.debug(f"Added user {member.name} in database")

        logger.info(f"Logged in as {self.user} (ID: {self.user.id}) on server {server.name}")

    async def on_message(self, message: nextcord.message.Message):
        await self.process_commands(message)

        if not message.author.bot:
            logger.debug(f"Member {message.author} in {message.channel} channel leave message: {message.content}")


class Command(BaseCommand):
    help = "Runing bot command"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.members = True
        client = Client(command_prefix="!", intents=intents)
        client.load_extension("guilds.management.commands.cogs.terror")
        client.load_extension("guilds.management.commands.cogs.clone")
        client.load_extension("guilds.management.commands.cogs.fast_trade")
        client.run(settings.TOKEN)
