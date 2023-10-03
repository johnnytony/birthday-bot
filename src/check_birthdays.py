import asyncio

from re import U
import requests
import discord
import sys

from discord import Guild

import json
import datetime

from discord.ext import tasks

import configs

import time

base_url = configs.BASE_URL
headers = {'Content-Type': 'application/json', 'API-Key':configs.API_KEY}

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():

    print(f'Logged in as {client.user}')
    
    channel = client.get_channel(int(configs.CHANNEL_ID))

    url = base_url + '/check_birthdays'

    r = requests.get(url, headers=headers)

    if r.status_code == 404:
        sys.exit()

    data = r.json()

    guild = client.get_guild(int(configs.SERVER_ID))

    users_info = []

    for user in data:
        member = guild.get_member(int(user['id']))
        username = member.nick

        if not username:
            u = await client.fetch_user(int(user['id']))
            username = u.display_name

        date = datetime.datetime.strptime(user['birthday'],'%Y-%m-%d')
        years = str(datetime.date.today().year - date.year)

        users_info.append({'username': username, 'years': years})

    await channel.send('@everyone')

    for user_info in users_info:
        embed = discord.Embed(title=f'Happy Birthday {user_info["username"]}!',
                        description=f'Today our comrade `{user_info["username"]}` accomplish `{user_info["years"]} years old`!\nWe wish him/her a wonderful day!',
                        color=0xFF5733)

        embed.set_image(url="https://i.redd.it/5lbchzbtl8331.png")
        await channel.send(embed=embed)

    sys.exit()
    

client.run(configs.CLIENT_ID)


