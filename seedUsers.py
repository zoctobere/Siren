from discord.ext import commands
from builtins import bot
import db
import config

@bot.command()
async def getroles(ctx):

    print(ctx.author.id)
    print(config.superUsers)

    if ctx.channel.id != config.adminChannel:
        return

    if not ctx.author.id in config.superUsers:
        await ctx.send("Only Zoe, leggy, or Schala can run this command for security reasons.")
        return

    roles = ctx.guild.roles
    print(roles)
    await ctx.message.delete()

@bot.command()
async def seedusers(ctx):

    if ctx.channel.id != config.adminChannel:
        return

    if not ctx.author.id in config.superUsers:
        await ctx.send("Only Zoe, leggy, or Schala can run this command for security reasons.")
        return

    role = ctx.guild.get_role(config.restreamRole)
    members = role.members

    membersSeeded = 0

    await ctx.send('Seeding users with the ' + role.name + ' role...')

    for member in members:
        if db.doesUserExist(member.name):
            continue
        else:
            db.addUser(member.name, member.id, member.mention)
            membersSeeded += 1
    await ctx.send(str(membersSeeded) + ' users with the `' + role.name + '` role added to the database.')

    await ctx.message.delete()
