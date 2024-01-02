import asyncio
from datetime import datetime

import pytest
import pytest_django
from asgiref.sync import sync_to_async
from django.utils import timezone

from guilds.models import Channels, Roles, Settings
from users.models import DiscordUser

from .fake_bot import FakeBot
from .fake_guild import FakeChannel, FakeGuild, FakeRole


@pytest.fixture
def bot():
    guild = FakeGuild()

    everyone_role = FakeRole(id=0, name="everyone")
    admin_role = FakeRole(id=1, name="Administrator")
    moder_role = FakeRole(id=2, name="Moderator")
    guild.add_roles([everyone_role, admin_role, moder_role])

    guild.add_channel(id=665544, name="clone_channel")

    guild.add_member(
        id=99887701,
        name="user1",
        display_name="User 1",
        discriminator=0,
        bot=False,
        joined_at=datetime(
            2022, 5, 6, 10, 0, 0, tzinfo=timezone.get_current_timezone()
        ),
        removed_at=None,
        roles=[everyone_role, admin_role],
    )
    bot = FakeBot()
    bot.add_guild(guild)
    return bot


@pytest.mark.asyncio
async def test_bot_guild_id(bot):
    assert bot.guilds.pop().id == 1234567890


@pytest.mark.asyncio
@pytest.mark.django_db()
async def test_bot_on_ready(bot):
    await bot.on_ready()

    settings = await Settings.objects.afirst()
    assert settings.id == 1234567890
    assert settings.name == "TestDiabloBotGuild"

    role = await Roles.objects.aget(id=1)
    assert role.id == 1
    assert role.name == "Administrator"

    channel = await Channels.objects.aget(id=665544)
    assert channel.id == 665544
    assert channel.name == "clone_channel"

    user = await DiscordUser.objects.aget(id=99887701)
    assert user.id == 99887701
    assert user.username == "user1"
