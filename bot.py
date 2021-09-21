import os
import discord
import hashlib

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = discord.Client()

def encrypt_string(str):
    encoded = str.encoded()
    result = hashlib.sha256(encoded)

    return result.digest()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.environ.get('SECRET_KEY'))