import datetime, requests, json
from random import choice, getrandbits
from discord.ext import commands, tasks
from discord import Game, Activity, ActivityType, Embed
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

class Loops(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

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
	
	@tasks.loop(minutes=1)
	async def reminders(self):
		await self.bot.wait_until_ready()
		data = db.collection('Reminders').document('Reminders').get().get('Reminders')
		now = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%d-%m-%Y-%H-%M')    
		for reminder in data:
			if (str(reminder['time']) == str(now)):
				Logging.info(f"Reminding {reminder['mention']} about {reminder['title']}")
				await self.bot.get_channel(866711571120390144).send(f"<@{reminder['mention']}> Reminder: `{reminder['title']}`")
	"""
	@tasks.loop(hours=12)
	async def bgs(self):
		await self.bot.wait_until_ready()
		stations = requests.get('https://elitebgs.app/api/ebgs/v5/systems?faction=estra%20haven').json()

		embed = Embed(
			title="BGS INFO",
            color=0xff0000
		)
		for idocs in range(0, len(stations['docs'])):
			embed.add_field(
				name=stations['docs'][idocs]['name'],
				value=f"State of {stations['docs'][idocs]['state']}",
				inline=False
				#stations['docs'][idocs]['conflicts'][iconflicts]['type']
			)
		
		embed.set_footer(text='This code is ruined by ThiJNmEnS#6669')
		await self.bot.get_channel(867119192028479488).send(embed=embed)
	"""
	@commands.Cog.listener()
	async def on_ready(self):
		self.status.start()
		self.reminders.start()
		#self.bgs.start()

def setup(bot):
	bot.add_cog(Loops(bot))