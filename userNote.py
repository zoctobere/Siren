from discord.ext import commands
from builtins import bot
import db
import config

@bot.command()
async def addnote(ctx, arg1, arg2):

    if ctx.channel.id != config.adminChannel:
        return

    if ctx.author.id in config.superUsers:
        ctx.send("Only Zoe, leggy, or Schala can run this command for security reasons.")
        return

    if not db.doesUserExist(arg1):
        await ctx.send('```' + arg1 + ' is not in the database. Please check the spelling and try again. If this is a new restream team member, have Zoe reseed the db.```')
        await ctx.message.delete()
        return

    db.setUserField(arg1, 'note', arg2)

    await ctx.send('```Note added for ' + arg1 + '.\n\nNote Contents: ' + arg2 + '```')

@addnote.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the user and the note you wish to add (enclosed in quotes). Usage: .addnote <username> <"This is an example note.">```')
        await ctx.message.delete()
