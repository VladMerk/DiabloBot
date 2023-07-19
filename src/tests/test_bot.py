import asyncio
import pytest
import pytest_django

from asgiref.sync import sync_to_async
from guilds.models import Settings, Roles, Channels
from users.models import DiscordUser

from .fake_bot import FakeBot
from .fake_guild import FakeRole, FakeGuild


@pytest.fixture
def bot():
    return FakeBot()


@pytest.mark.asyncio
async def test_bot_guild_id(bot):
    assert bot.guilds.pop().id == 1234567890

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_bot_on_ready(bot):
    await bot.on_ready()

    settings = await Settings.objects.afirst()
    assert settings.id == 1234567890
    assert settings.name == 'TestDiabloBotGuild'

    role = await Roles.objects.aget(id=1)
    assert role.id == 1
    assert role.name == 'Administrator'

    channel = await Channels.objects.aget(id=665544)
    assert channel.id == 665544
    assert channel.name == 'clone_channel'

    user = await DiscordUser.objects.aget(id=99887701)
    assert user.id == 99887701
    assert user.username == 'User 1'

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_some_function():
    s = await Settings.objects.afirst()
    print(s.id)
