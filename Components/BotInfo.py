import requests, re
from discord.ext import commands
from discord import Embed
from Components.Logging import Logging
from firebase_admin import firestore

db = firestore.client()

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

def setup(bot):
    bot.add_cog(BotInfo(bot))