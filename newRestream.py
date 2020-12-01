import discord
import datetime
import pprint

import events
import db
import getDateFromDay as nd

from random import randrange

async def createRestream(arg, author):

    event = events.events[arg]
    restreamDate = nd.next_weekday(event['day'])

    embedTitle = event['name'] + ' @ ' + event['startTime'] + ' on ' + event['channel'] +  ' - ' + restreamDate.strftime('%m/%d')
    embedDescription = 'If you would like to sign up, please react with the emoji corresponding to the roles you are interested in volunteering for.'

    # Generate random restramID and use as color
    embedColor = randrange(0x0, 0xFFFFFF)
    restreamID = str(hex(embedColor)[2:8]).upper().rjust(6, '0')

    # Make sure restreamID is unique
    while db.doesRestreamExist(restreamID):
        embedColor = randrange(0x0, 0xFFFFFF)
        restreamID = str(hex(embedColor)[2:8]).upper()

    embed = discord.Embed(title=('Signups for ' + embedTitle), description=embedDescription, color=embedColor)
    embed.add_field(name='----------------', value='🎙 -- **Commentary**\n\n📌 -- **Tracking**\n\n🖥 -- **Restreaming**', inline=True)
    embed.set_footer(text='Signups opened by: ' + author + ' | Restream ID: ' + restreamID + ' | Status: Accepting Volunteers')

    raceConfirmation = '```Restream created with ID: ' + restreamID + '\n\n' + embedTitle + '```'

    data = { 'event': event,
             'ID': restreamID,
             'date': restreamDate.strftime('%m/%d/%y'),
             'confirmation': raceConfirmation,
             'embed': embed,
             'embedTitle': embedTitle,
             'color': embedColor}

    return data;
