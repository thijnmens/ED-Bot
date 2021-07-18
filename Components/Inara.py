import datetime, json, requests
from Components.Logging import *
from discord import Embed
from discord.ext import commands
from os import getenv, getcwd
from dotenv import load_dotenv
import inspect


EDDN_Relay = 'tcp://eddn.edcd.io:9500'
EDDN_Timeout = 600000

fakeresponce = {
   'eventCustomID': 13458,
   'eventStatus': 200,
   'eventData': {
       'userID': 1,
       'userName': 'Artie',
       'commanderName': 'Artie',
       'commanderRanksPilot': [
           {
               'rankName': 'combat',
               'rankValue': 7,
               'rankProgress': 0.40000000000000002
           },
           {
               'rankName': 'trade',
               'rankValue': 8,
               'rankProgress': 1
           },
           {
               'rankName': 'exploration',
               'rankValue': 6,
               'rankProgress': 0.11
           },
           {
               'rankName': 'cqc',
               'rankValue': 2,
               'rankProgress': 0.089999999999999997
           },
           {
               'rankName': 'empire',
               'rankValue': 12,
               'rankProgress': 0.17000000000000001
           },
           {
               'rankName': 'federation',
               'rankValue': 11,
               'rankProgress': 0.65000000000000002
           }
       ],
       'preferredAllegianceName': 'Independent',
       'preferredPowerName': 'Felicia Winters',
       'commanderMainShip': {
           'shipType': 'federation_corvette',
           'shipName': 'Spectre',
           'shipIdent': 'X-0QAR',
           'shipRole': ''
       },
       'commanderSquadron': {
           'SquadronID': 5,
           'SquadronName': 'Inara Test Wing',
           'SquadronMembersCount': 8,
           'SquadronMemberRank': 'Squadron commander',
           'inaraURL': 'https:\/\/inara.cz\/squadron\/5\/'
       },
       'preferredGameRole': 'Freelancer',
       'avatarImageURL': 'https:\/\/inara.cz\/data\/users\/0\/1x1548.jpg',
       'inaraURL': 'https:\/\/inara.cz\/cmdr\/1\/',
       'otherNamesFound': [
                    'Artiex2',
                    'Artieblahblah'
       ]
   }
}

load_dotenv(f'{getcwd()}/config.env')


class Inara(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['Get_Commander', 'cmdr'])
    async def Get_Cmdr(self, ctx, cmdr_name):
        try:
            params = {
                'header': {
                    'appName': 'RogueBot',
                    'appVersion': '0.0.1',
                    'isBeingDeveloped': True,
                    'APIkey': str(getenv('INARAKEY')),
                    'commanderName': 'Thijnmens',
                    'commanderFrontierID': '8017135'
                },
                'events': [
                    {
                        'eventName': 'getCommanderProfile',
                        'eventTimestamp': str(datetime.datetime.now().strftime('%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')),
                        'eventData': {
                            'searchName': cmdr_name
                        }
                    }
                ]
            }
            params = json.dumps(params)
            response = requests.post(url='https://inara.cz/inapi/v1/', data=params)
            data = response.json()
            Logging.info(data['events'][0]['eventData']['userName'])
            embed = Embed(
                title=f"Cmdr {data['events'][0]['eventData']['commanderName']}",
                url=f"https://inara.cz/cmdr/{data['events'][0]['eventData']['userID']}",
                description=data['events'][0]['eventData']['preferredGameRole'],
                color=0xff0000
            )
            embed.add_field(
                name="Combat",
                value=data['events'][0]['eventData']['commanderRanksPilot'][0]['rankValue'],
                inline=True
            )
            embed.add_field(
                name="Trade",
                value=data['events'][0]['eventData']['commanderRanksPilot'][1]['rankValue'],
                inline=True
            )
            embed.add_field(
                name="Exploration",
                value=data['events'][0]['eventData']['commanderRanksPilot'][2]['rankValue'],
                inline=True
            )
            embed.add_field(
                name="CQC",
                value=data['events'][0]['eventData']['commanderRanksPilot'][3]['rankValue'],
                inline=True
            )
            embed.add_field(
                name="Empire",
                value=data['events'][0]['eventData']['commanderRanksPilot'][4]['rankValue'],
                inline=True
            )
            embed.add_field(
                name="Federation",
                value=data['events'][0]['eventData']['commanderRanksPilot'][5]['rankValue'],
                inline=True
            )
            embed.set_thumbnail(url=data['events'][0]['eventData']['avatarImageURL'])
            embed.set_footer(text='This code is ruined by ThiJNmEnS#6669')
            await ctx.send(embed=embed)

        except Exception as e:
            Logging.error(e)

def setup(bot):
    bot.add_cog(Inara(bot))