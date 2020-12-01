from discord.ext import commands
from builtins import bot
import db
import config

@bot.command()
async def setcommentary(ctx, arg1, arg2, arg3):

    if ctx.channel.id != config.adminChannel:
        return

    if not db.doesRestreamExist(arg1):
        await ctx.send('```No restream found with Restream ID: ' + arg1 + '```')
        await ctx.message.delete()
        return

    if not db.isRestreamOpen(arg1):
        if not ctx.author.id in config.superUsers:
            await ctx.send('```Restream ' + arg1 + ' is not open. Please check the Restream ID and try again.```')
            await ctx.message.delete()
            return

    if not db.doesUserExist(arg2) or not db.doesUserExist(arg3):
        if not db.doesUserExist(arg2):
            await ctx.send('```' + arg2 + ' is not in the database. Please check the spelling and try again. If this is a new restream team member, have Zoe reseed the db.```')
        if not db.doesUserExist(arg3):
            await ctx.send('```' + arg3 + ' is not in the database. Please check the spelling and try again. If this is a new restream team member, have Zoe reseed the db.```')
        await ctx.message.delete()
        return

    db.setRestreamField(arg1, 'commentary1', arg2)
    db.setRestreamField(arg1, 'commentary2', arg3)

    await ctx.send('```Commentary for Restream ' + arg1 + ' set to: ' + arg2 + ', ' + arg3 + ' by ' + ctx.author.name + '.```')

    await ctx.message.delete()

@setcommentary.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the Restream ID and BOTH commentators separated by a space. Usage: .setcommentary <restreamID> <commentary1> <commentary2>```')
        await ctx.message.delete()

@bot.command()
async def settracker(ctx, arg1, arg2):

    if ctx.channel.id != config.adminChannel:
        return

    if not db.doesRestreamExist(arg1):
        await ctx.send('```No restream found with Restream ID: ' + arg1 + '```')
        await ctx.message.delete()
        return

    if not db.isRestreamOpen(arg1):
        if not ctx.author.id in config.superUsers:
            await ctx.send('```Restream ' + arg1 + ' is not open. Please check the Restream ID and try again.```')
            await ctx.message.delete()
            return

    if not db.doesUserExist(arg2):
        await ctx.send('```' + arg2 + ' is not in the database. Please check the spelling and try again. If this is a new restream team member, have Zoe reseed the db.```')
        await ctx.message.delete()
        return

    db.setRestreamField(arg1, 'tracker', arg2)

    await ctx.send('```Tracker for Restream ' + arg1 + ' set to ' + arg2 + ' by ' + ctx.author.name + '.```')

    await ctx.message.delete()

@settracker.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the Restream ID and tracker. Usage: .settracker <restreamID> <tracker>```')
        await ctx.message.delete()

@bot.command()
async def setrestreamer(ctx, arg1, arg2):

    if ctx.channel.id != config.adminChannel:
        return

    if not db.doesRestreamExist(arg1):
        await ctx.send('```No restream found with Restream ID: ' + arg1 + '```')
        await ctx.message.delete()
        return

    if not db.isRestreamOpen(arg1):
        if not ctx.author.id in config.superUsers:
            await ctx.send('```Restream ' + arg1 + ' is not open. Please check the Restream ID and try again.```')
            await ctx.message.delete()
            return

    if not db.doesUserExist(arg2):
        await ctx.send('```' + arg2 + ' is not in the database. Please check the spelling and try again. If this is a new restream team member, have Zoe reseed the db.```')
        await ctx.message.delete()
        return

    db.setRestreamField(arg1, 'restreamer', arg2)

    await ctx.send('```Restreamer for Restream ' + arg1 + ' set to ' + arg2 + ' by ' + ctx.author.name + '.```')

    await ctx.message.delete()

@setrestreamer.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the Restream ID and restreamer. Usage: .setrestreamer <restreamID> <restreamer>```')
        await ctx.message.delete()
