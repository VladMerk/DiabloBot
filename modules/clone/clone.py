from nextcord.ext import commands, tasks
import aiohttp
from modules.configs.config import token_d2r, clone_discord_channel
from modules.loggers import logger


class Clone(commands.Cog, name='Clone Diablo'):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.url = 'https://d2runewizard.com/api/diablo-clone-progress/all'
        self.params = {'token': token_d2r}
        self.progress = {}
        self.clone_dict = {}
        self.flag = 0
        self.region = {1: 'America',  2: 'Europe',   3: 'Asia'}
        self.ladder = {1: 'Ladder',   2: 'NonLadder'}
        self.hc = {1: 'Hardcore', 2: 'Softcore'}
        self.clone.start()


    async def get_json(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url, params=self.params) as r:

                rjson = await r.json()

                self.progress = {item['server']: {'server': item['server'],
                                    'progres': item['progress'],
                                    'ladder': item['ladder'],
                                    'hardcore': item['hardcore'],
                                    'region': item['region'],
                                    'lastUpdate': item['lastUpdate']['seconds']}
                        for item in rjson['servers']}

    def get_message(self, prg: list) -> str:
        message = ''
        if self.flag:
            message += '\nПоследнее изменение:\n'
            message += self.get_server(prg=prg, servers=[prg[self.top_clone_server]['server']])

        message += '***Ladder***\n'
        message += self.get_server(prg=prg, servers=['ladderSoftcoreAsia', 'ladderSoftcoreEurope', 'ladderSoftcoreAmericas'])
        message += self.get_server(prg=prg, servers=['ladderHardcoreAsia', 'ladderHardcoreEurope', 'ladderHardcoreAmericas'])

        message += '***NonLadder***\n'
        message += self.get_server(prg=prg, servers=['nonLadderSoftcoreAsia', 'nonLadderSoftcoreEurope', 'nonLadderSoftcoreAmericas'])
        message += self.get_server(prg=prg, servers=['nonLadderHardcoreAsia', 'nonLadderHardcoreEurope', 'nonLadderHardcoreAmericas'])

        message += f'\nProvided By <https://d2runewizard.com>'

        return message

    def get_server(self, prg: dict, servers: list) -> str:
        mess = ''
        for server in servers:
            if int(prg[server]['progres']) > 1:
                mess += f"**[{prg[server]['progres']}/6]** "
            else:
                mess += f"[{prg[server]['progres']}/6] "
            mess += f"{'Ladder' if prg[server]['ladder'] else 'NonLadder'} "
            mess += f"{'Hardcore' if prg[server]['hardcore'] else 'Softcore'} "
            mess += f"{prg[server]['region']} "
            mess += f"<t:{prg[server]['lastUpdate']}:R>\n"
        return mess + '\n'


    @tasks.loop(seconds=30)
    async def clone(self):
        channel = self.bot.get_channel(clone_discord_channel)
        await self.get_json()
        if self.clone_dict != {}:
            for server in self.progress:
                if self.clone_dict[server]['progres'] != self.progress[server]['progres']:
                    self.top_clone_server = server
                    self.flag = 1
                    self.clone_dict = self.progress
                    break
        else:
            self.clone_dict = self.progress
            await channel.purge()
            await channel.send(self.get_message(prg=self.progress))

        if self.flag:
            await channel.purge()
            await channel.send(self.get_message(prg=self.progress))
            self.flag = 0



    @clone.before_loop
    async def befor_clone(self):
        await self.bot.wait_until_ready()



def setup(bot: commands.Bot):
    bot.add_cog(Clone(bot=bot))
