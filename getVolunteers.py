from discord.ext import commands
from builtins import bot
import db
import config

@bot.command()
async def getvolunteers(ctx, arg):

    if ctx.channel.id != config.adminChannel:
        return

    if not db.doesRestreamExist(arg):
        await ctx.send('```No restream found with Restream ID: ' + arg + '```')
        await ctx.message.delete()
        return

    if not db.isRestreamOpen(arg):
        if not ctx.author.id in config.superUsers:
            await ctx.send('```Restream ' + arg + ' is not open. Please check the Restream ID and try again.```')
            await ctx.message.delete()
            return

    # TODO: check for siren admin and/or restream lead+
    roles = { 0: '\n----------------\n🎙 - Commentary Volunteers:\n\n',
              1: '\n----------------\n📌 - Tracker Volunteers:\n\n',
              2: '\n----------------\n🖥 - Restreamer Volunteers:\n\n'}
    reactionNum = 0

    messageID = db.getRestreamField(arg, 'messageID')
    message = await ctx.guild.get_channel(config.signupChannel).fetch_message(messageID)

    volunteerList = '```\nList of Volunteers for Restream ' + arg + ' (' + message.embeds[0].title + '):\n\n(Username -- Date Last Assigned to Restream (if known))\n'

    for reaction in message.reactions:
        if reaction.me:
            volunteerList += roles[reactionNum]
            users = await reaction.users().flatten()
            for user in users:
                if user.bot:
                    continue
                volunteerList += user.name
                if db.doesUserExist(user.name):
                    lastAssigned = db.getUserField(user.name, 'lastAssigned')
                    note = db.getUserField(user.name, 'note')
                    if lastAssigned != '':
                        volunteerList += (' -- ' + lastAssigned)
                    if note != '':
                        volunteerList += (' -- ' + note)
                volunteerList += '\n'
            reactionNum += 1
        else:
            print('Ignoring ' + reaction.emoji + '.')

    volunteerList += '```'

    await ctx.author.send(volunteerList)
    await ctx.message.delete()

@getvolunteers.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the Restream ID you wish to retrieve volunteers for. Usage: .getvolunteers <restreamID>```')
        await ctx.message.delete()
