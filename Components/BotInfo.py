import requests, re
from random import choice, getrandbits
from discord.ext import commands, tasks
from discord import Game, Activity, ActivityType, Embed
from Components.Logging import Logging

play_status_list = [
    "Elite Dangerous",
	"Nekopara Vol 1",
	"Nekopara Vol 2",
	"Nekopara Vol 3",
	"Nekopara Vol 4"
]

watch_status_list = [
    "hentai",
    "Nekopara",
    "notmyname stream hentai",
    "You."
]

class BotInfo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(invoke_without_command=True, aliases=['botinfo'])
	async def Info(self, ctx):
		commit_count = re.search('\d+$', requests.get('https://api.github.com/repos/thijnmens/RogueBot/commits?per_page=1').links['last']['url']).group()
		await ctx.send(commit_count)
	
	@commands.command(invoke_without_command=True, aliases=[])
	async def Ping(self, ctx):
		await ctx.send(f'Ping Pong `{round(self.bot.latency * 1000)}ms`')
	
	@commands.group(invoke_without_command=True, aliases=['h'])
	async def Help(self, ctx):
		embed = Embed(
			title="Help",
			description="[Discord](https://discord.gg/KHcWH3jD) | [Rogue Bot Repo](https://github.com/thijnmens/RogueBot)",
            color=0xff0000
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/865588554603298816/c124b4a1595f81d545e5431554ee4af3.png")
		embed.set_footer(text='This code is ruined by ThiJNmEnS#6669')
		await ctx.send(embed=embed)

	@tasks.loop(hours=1)
	async def status(self):
		await self.bot.wait_until_ready()
		if getrandbits(1) == 1:
			value = choice(play_status_list)
			await self.bot.change_presence(activity=Game(name=value))
			Logging.info(f"Status set to: {value}")
		else:
			value = choice(watch_status_list)
			await self.bot.change_presence(activity=Activity(name=value, type=ActivityType.watching))
			Logging.info(f"Status set to: {value}")

	@commands.Cog.listener()
	async def on_ready(self):
		self.status.start()

def setup(bot):
    bot.add_cog(BotInfo(bot))