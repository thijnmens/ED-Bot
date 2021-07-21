from dotenv import load_dotenv
from os import getcwd, getenv
from discord import Intents, AllowedMentions
from discord.ext import commands
from Components.Logging import Logging
from firebase_admin import credentials, initialize_app

# Load Env Vars
cwd = getcwd()
load_dotenv(f'{cwd}/config.env')

# Login to firebase
cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "roguebot-5faa0",
        "private_key_id": "f2b7c606f0901e0d2c0a4b510423278c45b15a64",
        "private_key": getenv("PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": "firebase-adminsdk-kg3uk@roguebot-5faa0.iam.gserviceaccount.com",
        "client_id": "103888085591896301152",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-kg3uk%40roguebot-5faa0.iam.gserviceaccount.com"
})
default_app = initialize_app(cred)

# Define Bot
intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', help_command=None, intents=intents, case_insensitive=True, allowed_mentions=AllowedMentions(replied_user=False))

# Definition Cogs
initial_cogs = [
    "jishaku",
    "Components.Inara",
    "Components.BotInfo",
    "Components.ErrorHandler",
    "Components.Random",
    "Components.Loops"
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
    Logging.info(f'''------------------------------\n   Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\n    Args: {ctx.args}''')

@bot.after_invoke
async def after_invoke(ctx):
    Logging.info(f'Concluded {ctx.command}')

# Discord Login
bot.run(getenv("TOKEN"))