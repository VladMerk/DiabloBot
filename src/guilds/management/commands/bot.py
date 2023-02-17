import logging

import nextcord
import redis
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from nextcord.ext import commands

from guilds.models import Channels, Roles, Settings
from users.models import User

logger = logging.getLogger(__name__)


class Client(commands.Bot):
    # 1023904638992396330
    async def check_redis(self):
        try:
            # FIXME Определить настройку адреса сервера в settings.py
            r = redis.Redis(host="127.0.0.1", port=6379)
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
                _member, created = await sync_to_async(User.objects.get_or_create)(
                    id=member.id,
                    username=member.name,
                    discriminator=member.discriminator,
                )
                if created:
                    logger.info(f"Member {_member.username} is created.")

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
        # TODO Добавить фильтр на сообщения от бота
        await self.process_commands(message)

        logger.debug(f"Member {message.author} in {message.channel} channel leave message: {message.content}")

        _data = await Settings.objects.afirst()

        if message.channel in [_data.terror_channel_id, _data.clone_channel_id]:
            await message.publish()
            return

        if message.channel.id == _data.fasttrade_channel_id:
            server = self.get_guild(_data.id)
            role = nextcord.utils.get(server.roles, id=_data.fasttrade_channel_role_id)
            logger.debug(role)
            for member in server.members:
                if role in member.roles and message.author != member:
                    if len(message.attachments):
                        mess = f"{message.author.mention} в канале {message.channel.mention} оставил сообщение:"
                        f"`{message.content}`"
                        for attach in message.attachments:
                            mess += f"{attach.url}\n"
                        await member.send(mess)
                    else:
                        await member.send(
                            f"{message.author.mention} в канале {message.channel.mention} оставил сообщение:" f" `{message.content}`"
                        )
                    return


class Command(BaseCommand):
    help = "Runing bot command"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        intents = nextcord.Intents.default()
        intents.message_content = True
        client = Client(command_prefix="!", intents=intents)
        client.load_extension("guilds.management.commands.cogs.terror")
        client.load_extension("guilds.management.commands.cogs.clone")
        client.load_extension("guilds.management.commands.cogs.fast_trade")
        client.run(settings.TOKEN)
