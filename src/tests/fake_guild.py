from datetime import datetime
from typing import List, Optional, TypedDict
import nextcord
from unittest import mock

from django.utils import timezone

from nextcord.member import Member
from nextcord.role import Role
from nextcord.abc import GuildChannel
from nextcord.types.guild import Guild as GuildPayload


class FakeChannel(GuildChannel):

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.type = 1


class FakeRole(nextcord.Role):

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class FakeMember:

    # def __init__(self, guild, data: dict) -> None:
    #     super().__init__(state=None, guild=guild, data=data)
    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self):
        return self.name

    @property
    def id(self) -> int:
        return self._data.get('id')

    @property
    def name(self) -> str:
        return self._data.get('name')

    @property
    def display_name(self) -> str:
        return self._data.get('display_name')

    @property
    def discriminator(self) -> str:
        return self._data.get('discriminator')

    @property
    def bot(self) -> bool:
        return self._data.get('bot')

    @property
    def joined_at(self) -> datetime:
        return self._data.get('joined_at')


class FakeGuild(nextcord.Guild):
    def __init__(self, *args, **kwargs):
        self.id = 1234567890
        self.name = 'TestDiabloBotGuild'

    @property
    def channels(self) -> List[GuildChannel]:
        channel1 = FakeChannel(665544, 'clone_channel')
        channel2 = FakeChannel(665588, 'terror_channel')
        channel3 = FakeChannel(665577, 'fast_trade_channel')
        return [channel1, channel2, channel3]

    @property
    def members(self) -> List[Member]:
        member_list = []
        for i in range(1, 4):
            data = {
                'id':99887700+i,
                'name': f'User {i}',
                'display_name': f'User {i}',
                'discriminator': f'445{i}',
                'bot':False,
                'joined_at':timezone.make_aware(timezone.datetime(2000, i, 1, 10, 0, 0),
                                                timezone.get_current_timezone())
            }
            member = FakeMember(data=data)
            member_list.append(member)
        return member_list

    @property
    def roles(self) -> List[Role]:
        everyone = FakeRole(id=0, name='everyone')
        administator = FakeRole(id=1, name='Administrator')
        moderator = FakeRole(id=2, name='Moderator')

        return [
            everyone,
            administator,
            moderator
        ]

    def member_count(self) -> int | None:
        return len(self.members)
