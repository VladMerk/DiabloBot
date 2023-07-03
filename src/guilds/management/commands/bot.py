import logging

import nextcord
import redis
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
# from django.db.utils import IntegrityError
from nextcord.ext import commands

from guilds.models import Channels, Roles, Settings
from users.models import User

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
        server = self.get_guild(server.id)

        _settings, created = await sync_to_async(Settings.objects.get_or_create)(id=server.id, name=server.name)
        if created:
            logger.info(f"Settings server {server} is created")

        for member in server.members:
            if not member.bot:
                # FIXME почему не срабатывает "взять или создать" ?
                # TODO https://docs.djangoproject.com/en/4.1/ref/models/options/#unique-together
                # TODO https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
                try:
                    _member, created = await sync_to_async(User.objects.get_or_create)(
                        id=member.id,
                        username=member.name,
                        discriminator=member.discriminator,
                    )
                    if created:
                        logger.info(f"Member {_member.username} is created.")
                # IntegrityError
                except Exception:
                    logger.warning(f"User: {member} is not unique")

        for channel in server.channels:
            if channel.type != 4:
                # 4 == группы каналов
                _channel, created = await sync_to_async(Channels.objects.get_or_create)(id=channel.id, name=channel.name)
                if created:
                    logger.info(f"Channel {channel.name} is created.")

        for role in server.roles:
            _role, created = await sync_to_async(Roles.objects.get_or_create)(id=role.id, name=role.name)
            if created:
                logger.info(f"Role {role.name} is created.")

        logger.info(f"Logged in as {self.user} (ID: {self.user.id}) on server {server}")

    async def on_message(self, message: nextcord.message.Message):
        await self.process_commands(message)

        if not message.author.bot:
            logger.debug(f"Member {message.author} in {message.channel} channel leave message: {message.content}")

        _data = await Settings.objects.afirst()

        if message.channel.id in [_data.terror_channel_id, _data.clone_channel_id]:
            await message.publish()
            logger.debug(f"Message in {message.channel} channel is published.")
            return


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
