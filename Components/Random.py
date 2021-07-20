import datetime
from Components.Logging import Logging
from discord.ext import commands
from firebase_admin import firestore

db = firestore.client()

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['Set_Reminder', 'R', 'Remind'])
    async def reminder(self, ctx, title, *args):
        minutes = 0
        hours = 0
        days = 0
        weeks = 0
        [arg.lower() for arg in args]
        if ('-m' in args):
            index = args.index('-m')
            minutes = int(args[index+1])
        if ('-h' in args):
            index = args.index('-h')
            hours = int(args[index+1])
        if ('-d' in args):
            index = args.index('-d')
            days = int(args[index+1])
        if ('-w' in args):
            index = args.index('-w')
            weeks = int(args[index+1])
        data = db.collection('Reminders').document('Reminders').get().get('Reminders')
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        time_change = datetime.timedelta(minutes=minutes, hours=hours, days=days, weeks=weeks)
        reminder = now + time_change
        new_date = reminder.strftime('%d-%m-%Y')
        new_time = reminder.strftime('%H:%M')
        reminder = reminder.strftime('%d-%m-%Y-%H-%M')
        data.append({
            "time": reminder,
            "title": title,
            "mention": ctx.author.id
        })
        db.collection('Reminders').document('Reminders').set({"Reminders": data})
        await ctx.send(f'I will remind you for `{title}` on `{new_date}` at `{new_time} UTC`')

def setup(bot):
    bot.add_cog(Random(bot))