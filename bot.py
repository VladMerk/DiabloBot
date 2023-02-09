import nextcord
from nextcord.ext import commands
from nextcord.utils import get
from modules.configs.config import token, clone_discord_channel, terror_zone_discord_channel, fast_trade_discord_channel, fast_trade_role

from modules.loggers import logger


intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")
    logger.debug('Debug message')


@client.event
async def on_message(message: nextcord.message.Message):
    await client.process_commands(message)
    if message.channel.id in [clone_discord_channel, terror_zone_discord_channel]:
        await message.publish()

    if message.channel.id == fast_trade_discord_channel:

        for guild in client.guilds:
            role = get(guild.roles, id=fast_trade_role)
            for member in guild.members:
                if role in member.roles and message.author != member:
                    # logger.info(f"{message.content} -- {message.attachments.url}")
                    # await member.send(f"{message.author.mention} в канале {message.channel.mention} оставил сообщение: `{message.content}`")
                    if len(message.attachments):
                        mess = f"{message.author.mention} в канале {message.channel.mention} оставил сообщение: `{message.content}`\n"
                        for attach in message.attachments:
                            mess += f"{attach.url}\n"
                        await member.send(mess)
                    else:
                        await member.send(f"{message.author.mention} в канале {message.channel.mention} оставил сообщение: `{message.content}`")


client.load_extension('modules.clone.clone')
client.load_extension('modules.terror_zone.terror')
client.load_extension('modules.fast_trade.fast_trade')

client.run(token)
