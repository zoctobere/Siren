import discord
from builtins import client

async def sendMessage(content, channel):
    sentMessage = channel.send(content)
    return sentMessage

async def sendDM(content, user):
    user.send(content)
