from discord.ext import commands
from builtins import bot
import newRestream
import db
import config

@bot.command()
async def opensignupsA(ctx):

    if ctx.channel.id != config.adminChannel:
        return

    # TODO: check for siren admin and/or restream lead+

    data = { 'monday': await newRestream.createRestream('mondayWeekly', ctx.author.name),
             'tuesday': await newRestream.createRestream('urc', ctx.author.name),
             'wednesday': await newRestream.createRestream('mjc', ctx.author.name),
             'friday': await newRestream.createRestream('fridayWeekly', ctx.author.name),
             'saturday': await newRestream.createRestream('legacy', ctx.author.name)
             }
    for race in data:
        message = await ctx.guild.get_channel(config.signupChannel).send(embed=data[race]['embed'])
        await message.add_reaction('🎙')
        await message.add_reaction('📌')
        await message.add_reaction('🖥')

        db.addRestream(data[race]['ID'], data[race]['color'], message.id, data[race]['embedTitle'], data[race]['event'], data[race]['date'], ctx.author.name)

        # def addRaceDB(restreamID, messageID, event, raceDate, lead)

        await ctx.send(data[race]['confirmation'])
    await ctx.message.delete()

@bot.command()
async def opensignupsB(ctx):

    if ctx.channel.id != config.adminChannel:
        return

    # TODO: check for siren admin and/or restream lead+

    data = { 'sunday': await newRestream.createRestream('slapdash', ctx.author.name),
             'monday': await newRestream.createRestream('mondayWeekly', ctx.author.name),
             'thursday': await newRestream.createRestream('lrc', ctx.author.name),
             'friday': await newRestream.createRestream('fridayWeekly', ctx.author.name),
             'saturday': await newRestream.createRestream('legacy', ctx.author.name)
             }
    for race in data:
        message = await ctx.guild.get_channel(config.signupChannel).send(embed=data[race]['embed'])
        await message.add_reaction('🎙')
        await message.add_reaction('📌')
        await message.add_reaction('🖥')

        db.addRestream(data[race]['ID'], data[race]['color'], message.id, data[race]['embedTitle'], data[race]['event'], data[race]['date'], ctx.author.name)

        # def addRaceDB(restreamID, messageID, event, raceDate, lead)

        await ctx.send(data[race]['confirmation'])
    await ctx.message.delete()
