from datetime import datetime
from typing import List, Optional, TypedDict
from unittest import mock

import nextcord
from django.utils import timezone
from nextcord.abc import GuildChannel
from nextcord.member import Member
from nextcord.role import Role
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
    def __init__(
        self,
        id: int,
        name: str,
        display_name: str,
        discriminator: int,
        bot: bool,
        joined_at: datetime,
        removed_at: Optional[datetime],
        roles: list[FakeRole],
    ) -> None:
        self._id = id
        self._name = name
        self._display_name = display_name
        self._discriminator = discriminator
        self._bot = bot
        self._joined_at = joined_at
        self._removed_at = removed_at
        self._roles = roles

    def __str__(self):
        return self.name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def discriminator(self) -> str:
        return self._discriminator

    @property
    def bot(self) -> bool:
        return self._bot

    @property
    def joined_at(self) -> datetime:
        return self._joined_at

    @property
    def removed_at(self) -> Optional[datetime]:
        return self._removed_at

    @property
    def roles(self) -> List[FakeRole]:
        return self._roles


class FakeGuild(nextcord.Guild):
    def __init__(self, *args, **kwargs):
        self.id = 1234567890
        self.name = "TestDiabloBotGuild"
        self._channels = []
        self._roles = []
        self._members = []

    @property
    def channels(self) -> List[GuildChannel]:
        return self._channels

    def add_channel(self, id: int, name: str):
        self._channels.append(FakeChannel(id=id, name=name))

    @property
    def members(self) -> List[Member]:
        return self._members

    def add_member(
        self,
        id: int,
        name: str,
        display_name: str,
        discriminator: int,
        bot: bool,
        joined_at: datetime,
        removed_at: Optional[datetime],
        roles: List[FakeRole],
    ) -> None:
        self._members.append(
            FakeMember(
                id=id,
                name=name,
                display_name=display_name,
                discriminator=discriminator,
                bot=bot,
                joined_at=joined_at,
                removed_at=removed_at,
                roles=roles,
            )
        )

    @property
    def roles(self) -> List[Role]:
        return self._roles

    def add_role(self, role: FakeRole):
        self._roles.append(role)

    def add_roles(self, roles: List[FakeRole]):
        self._roles.extend(roles)

    def member_count(self) -> int | None:
        return len(self.members)
