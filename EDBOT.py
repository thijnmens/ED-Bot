from dotenv import load_dotenv
from os import getcwd, getenv
from discord import Intents, AllowedMentions
from discord.ext import commands
from Components.Logging import *

# Load Env Vars
cwd = getcwd()
load_dotenv(f'{cwd}/config.env')

# Define Bot
intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', help_command=None, intents=intents, case_insensitive=True, allowed_mentions=AllowedMentions(replied_user=False))

# Definition Cogs
initial_cogs = [
]

# Cog loading
for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        Logging.info(f'Successfully loaded {cog}')
    except Exception as e:
        Logging.error(f'Failed to load cog {cog}: {e}')

# Init Bot
@bot.event
async def on_ready():
    Logging.info(f'Bot has successfully launched as {bot.user}!')

@bot.before_invoke
async def before_invoke(ctx):
    Logging.info(f'''------------------------------\nInvoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}''')

@bot.after_invoke
async def after_invoke(ctx):
    Logging.info(f'Concluded {ctx.command}')

# Discord Login
bot.run(getenv("TOKEN"))