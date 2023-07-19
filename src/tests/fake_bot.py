from typing import List
import nextcord

from unittest import mock

from nextcord.guild import Guild
from guilds.management.commands.bot import Client
from .fake_guild import FakeGuild


class FakeBot(Client):

    def __init__(self):
        self.guild = FakeGuild()


    @property
    def guilds(self) -> List[Guild]:
        return [self.guild]

    @property
    def user(self):
        user = mock.MagicMock(spec=nextcord.User)
        user.id = 445566
        user.name = 'TestDiabloBot'
        return user

    async def fetch_guilds(self, *, limit: int | None = 200):
        return self.guilds
