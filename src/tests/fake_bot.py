from typing import List
from unittest import mock

import nextcord
from nextcord.guild import Guild

from guilds.management.commands.bot import Client

from .fake_guild import FakeGuild


class FakeBot(Client):
    def __init__(self):
        self._guilds = []

    @property
    def guilds(self) -> List[Guild]:
        return self._guilds

    def add_guild(self, guild: FakeGuild):
        self._guilds.append(guild)

    @property
    def user(self):
        user = mock.MagicMock(spec=nextcord.User)
        user.id = 445566
        user.name = "TestDiabloBot"
        return user

    async def fetch_guilds(self, *, limit: int | None = 200):
        return self.guilds
