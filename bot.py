from discord.ext import commands
import discord
import builtins
import config

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)
builtins.bot = bot

import openSignups
import getVolunteers
import setVolunteers
import checkVolunteers
import publishAssignments

import seedUsers
import userNote

@bot.event
async def on_ready():
    print('Beep boop. I am logged in and ready to go as {0.user}!'.format(bot))

@bot.command()
async def echo(ctx):
    return

bot.run(config.DISCORD_TOKEN)
