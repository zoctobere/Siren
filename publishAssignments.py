from discord.ext import commands
from builtins import bot
import db
import config
import discord

@bot.command()
async def publish(ctx, arg):

    if ctx.channel.id != config.adminChannel:
        return

    arg = arg.upper()

    if not db.doesRestreamExist(arg):
        await ctx.send('```No restream found with Restream ID: ' + arg + '```')
        await ctx.message.delete()
        return

    if not db.isRestreamOpen(arg):
        if not ctx.author.id in config.superUsers:
            if ctx.author.name != db.getRestreamField(arg, 'assignedBy'):
                await ctx.send('```Restream ' + arg + ' is not open. Please check the Restream ID and try again.```')
                await ctx.message.delete()
                return

    # Get volunteers from restream in DB

    volunteers = { 'commentary1': db.getRestreamField(arg, 'commentary1'),
                   'commentary2': db.getRestreamField(arg, 'commentary2'),
                   'tracker': db.getRestreamField(arg, 'tracker'),
                   'restreamer': db.getRestreamField(arg, 'restreamer')
                    }

    missingVolunteers = []
    hasMissingVolunteer = False

    for volunteer in volunteers:
        if volunteers[volunteer] == '':
            missingVolunteers.append(volunteer)
            hasMissingVolunteer = True

    if hasMissingVolunteer:
        missingVolunteersStr = ', '.join(map(str, missingVolunteers))
        await ctx.send('```Restream ' + arg + ' is missing the following volunteers: ' + missingVolunteersStr + '. Please set these volunteers and try again.```')
        await ctx.message.delete()
        return

    else:

        # Get mention str for each volunteer
        mentions = {}
        for volunteer in volunteers:
            mentions[volunteer] = db.getUserField(volunteers[volunteer], 'mention')

        embedTitle = db.getRestreamField(arg, 'displayTitle')
        embedDescription = '🎙 -- ' + mentions['commentary1'] + ' and ' + mentions['commentary2'] + '\n'
        embedDescription += '📌 -- ' + mentions['tracker'] + '\n'
        embedDescription += '🖥 -- ' + mentions['restreamer'] + '\n\n'
        embedDescription += '🐦 -- ' + bot.get_user(config.twitterOverlord).mention + '\n'
        embedColor = db.getRestreamField(arg, 'color')

        embed = discord.Embed(title=('Assignments for ' + embedTitle), description=embedDescription, color=embedColor)
        embed.set_footer(text='Assignments chosen by: ' + ctx.author.name + ' | Restream ID: ' + db.getRestreamField(arg, 'restreamID'))

        if db.isRestreamOpen(arg):


            assignmentMessage = await ctx.guild.get_channel(config.assignmentsChannel).send(embed=embed)

            db.setRestreamField(arg, 'assignmentID', assignmentMessage.id)


            signupMessage = await ctx.guild.get_channel(config.signupChannel).fetch_message(db.getRestreamField(arg, 'signupsID'))
            editedEmbed = signupMessage.embeds[0]
            footerText = editedEmbed.footer.text
            footerText = footerText.removesuffix('Accepting Volunteers')
            footerText += 'Volunteers Assigned'
            editedEmbed.set_footer(text=footerText)
            await signupMessage.edit(embed=editedEmbed)

            await ctx.send('```Assignments for Restream ' + arg + ' posted in #' + ctx.guild.get_channel(config.assignmentsChannel).name + '```\n' + assignmentMessage.jump_url)

            await ctx.message.delete()

            db.setRestreamField(arg, 'assignedBy', ctx.author.name)
            db.setRestreamField(arg, 'status', 'Closed')

            roleText = { 'commentary1': '-Commentary-',
                         'commentary2': '-Commentary-',
                         'tracker': '-Tracking-',
                         'restreamer': '-Restreaming-'
                        }

            for volunteer in volunteers:
                await bot.get_user(db.getUserField(volunteers[volunteer], 'id')).send('```You have been chosen for ' + roleText[volunteer] + ' for: \n\n' + embedTitle + '\n\nTo view the assignments for this restream, click the link below.```\n' + assignmentMessage.jump_url)
                db.setUserField(volunteers[volunteer], 'lastAssigned', db.getRestreamField(arg, 'date'))
            if config.overlordDM:
                await bot.get_user(config.twitterOverlord).send('```This is your Twitter reminder for: \n\n' + embedTitle + '\n\nTo view the assignments for this restream, click the link below.```\n\n' + assignmentMessage.jump_url)

        else:

            print('closed')
            assignmentMessage = await ctx.guild.get_channel(config.assignmentsChannel).fetch_message(db.getRestreamField(arg, 'assignmentID'))
            await assignmentMessage.edit(embed=embed)

            await ctx.send('```Assignments for Restream ' + arg + ' edited in #' + ctx.guild.get_channel(config.assignmentsChannel).name + '```\n' + assignmentMessage.jump_url)

            await ctx.message.delete()

            roleText = { 'commentary1': '-Commentary-',
                         'commentary2': '-Commentary-',
                         'tracker': '-Tracking-',
                         'restreamer': '-Restreaming-'
                        }

            for volunteer in volunteers:
                await bot.get_user(db.getUserField(volunteers[volunteer], 'id')).send('```Assignments have been updated for an existing restream.\n\nYou have been chosen for ' + roleText[volunteer] + ' for: \n\n' + embedTitle + '\n\nTo view the updated assignments for this restream, click the link below.```\n' + assignmentMessage.jump_url)
                db.setUserField(volunteers[volunteer], 'lastAssigned', db.getRestreamField(arg, 'date'))

@publish.error
async def clear_error(ctx, error):
    if ctx.channel.id != config.adminChannel:
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Please specify the Restream ID of the assignments you wish to publish. Usage: .publish <restreamID>```')
        await ctx.message.delete()
