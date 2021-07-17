import datetime, json, requests
from Components.Logging import *
from discord.ext import commands
from os import getenv, getcwd
from dotenv import load_dotenv

EDDN_Relay = 'tcp://eddn.edcd.io:9500'
EDDN_Timeout = 600000

load_dotenv(f'{getcwd()}/config.env')


class Inara(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['Get_Commander', 'cmdr'])
    async def Get_Cmdr(self, ctx, arg1):
        try:
            params = {
                'header': {
                    'appName': 'EDBOT',
                    'appVersion': '0.0.1',
                    'isBeingDeveloped': True,
                    'APIkey': str(getenv("INARAKEY")),
                    'commanderName': "Thijnmens",
                    'commanderFrontierID': '8017135'
                },
                'events': [
                    {
                        'eventName': 'getCommanderProfile',
                        'eventTimestamp': str(datetime.datetime.now().strftime('%Y-%m-%d' + 'T' + '%H:%M:2%S' + 'Z')),
                        'eventData': {
                            'searchName': arg1
                        }
                    }
                ]
            }
            params = json.dumps(params)
            Logging.info(params)
            responce = requests.post(url='https://inara.cz/inapi/v1/getCommanderProfile', params=params)
            Logging.info(responce)
            data = responce.json()
            Logging.info(data)

        except Exception as e:
            Logging.error(e)

def setup(bot):
    bot.add_cog(Inara(bot))