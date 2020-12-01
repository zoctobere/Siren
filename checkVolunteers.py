from discord.ext import commands
from builtins import bot
import db
import config

@bot.command()
async def checkvolunteers(ctx, arg):

    if ctx.channel.id != config.adminChannel:
        return

    arg = arg.upper()

    if not db.doesRestreamExist(arg):
        await ctx.send('```No restream found with Restream ID: ' + arg + '```')
        await ctx.message.delete()
        return

    content = '```Volunteer Details for Restream ' + arg + ':\n\n'
    content += ('Commentary: ' + db.getRestreamField(arg, 'commentary1') + ' & ' + db.getRestreamField(arg, 'commentary2') + '\n')
    content += ('Tracker: ' + db.getRestreamField(arg, 'tracker') + '\n')
    content += ('Restreamer: ' +db.getRestreamField(arg, 'restreamer') + '\n\n')
    if (db.getRestreamField(arg, 'status') == 'Open'):
        content += 'Restream Status: Accepting Volunteers```'
    else:
        content += 'Restream Status: Volunteers Assigned```'

    await ctx.send(content)

    await ctx.message.delete()

@checkvolunteers.error
async def clear_error(ctx, error):
    if ctx.channel.id != config.adminChannel:
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the Restream ID you wish to check volunteers for. Usage: .checkvolunteers <restreamID>```')
        await ctx.message.delete()
