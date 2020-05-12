
#.\env\Scripts\activate

# bot.py
import os
import hero
import discord
from dotenv import load_dotenv

from command import Command
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

c = Command()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    rsp = c.commandFront(msg)
    sLimit = 3
    if rsp:
        for idx,x in enumerate(rsp):
            if (idx < sLimit):
                await message.channel.send(x)


client.run(TOKEN)
