from re import S
import requests
import discord

import json
import datetime

from discord.ext import tasks

import configs

base_url = configs.BASE_URL
headers = {'Content-Type': 'application/json', 'API-Key':configs.API_KEY}

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        embed = discord.Embed(title='Commands',
                             description='Test out the birthday bot with the following commands',
                             color=0xFF5733)

        embed.add_field(name='_ _', value='_ _', inline=False)

        embed.add_field(name="Get all users birthday", value='`!birth all`',
                        inline=False)

        embed.add_field(name="Add or update a user birthday", value='`!birth add @example_username YYYY-mm-dd`',
                        inline=False)

        embed.add_field(name="Check for today's birthdays", value='`!birth today`')

        await message.channel.send(embed=embed)

    if message.content.startswith('!birth all'):
        url = base_url + '/list_birthdays'

        r = requests.get(url, headers=headers)

        data = r.json()

        if not r.json():
            await message.channel.send('No birthdays registered yet!')
            return


        embed = discord.Embed(title='Birthdays',
                             description="Here's a list of our fellow comrades birthday!",
                             color=0xFF5733)


        for i, user_birth in enumerate(data):
            user = await client.fetch_user(int(user_birth['id']))
            date = datetime.datetime.strptime(user_birth['birthday'],'%Y-%m-%d')

            embed.add_field(name=user.display_name, value=date.strftime("%d %B, %Y"), inline=False)
            
        await message.channel.send(embed=embed)


    if message.content.startswith('!birth add'):
        command = message.content
        command_args = command.split(' ')

        if len(command_args) != 4:
            await message.channel.send('Incorrect format for the command!')
            return

        user_id = int(command_args[2].replace('<@','').replace('>',''))
        
        user = await client.fetch_user(user_id)

        if not user:
            await message.channel.send("User specified doesn't exist!")
            return

        date = command_args[3]

        url = base_url + '/create_birthday'
        data = {'id': str(user.id), 'birthday': str(date)}
        

        r = requests.post(url, data=json.dumps(data), headers=headers)

        if  r.status_code == 400:
            date_errors =r.json()['birthday']

            for date_error in date_errors:
                await message.channel.send(date_error)
            return

        await message.channel.send(f'Birthday registered for {user.mention}!')


    if message.content.startswith('!birth today'):
        url = base_url + '/check_birthdays'

        r = requests.get(url, headers=headers)

        if r.status_code == 404:
            await message.channel.send(r.json()['detail'])
            return

        data = r.json()
        
        if len(data) == 1:
            user = await client.fetch_user(int(data[0]['id']))
            date = datetime.datetime.strptime(data[0]['birthday'],'%Y-%m-%d')
            years = datetime.date.today().year - date.year

            embed = discord.Embed(title=f'Happy Birthday {user.display_name}!',
                            description=f"Today our comrade `{user.display_name}` accomplish `{years} years old`!\nWe wish him/her a wonderful day!",
                            color=0xFF5733)

        else:
            users_data = [await client.fetch_user(int(user_data['id'])) for user_data in data]
            users_names = [user.display_name for user in users_data]
            
            date = datetime.datetime.strptime(data[0]['birthday'],'%Y-%m-%d')
            years = datetime.date.today().year - date.year

            joined_usernames = " and ".join(users_names)
            usernames = joined_usernames.replace(" and ", ", ", len(users_data) - 2)

            embed = discord.Embed(title=f'Happy Birthday {usernames}!',
                            description=f"Today our comrades `{usernames}` accomplish `{years} years old`!\nWe wish them a wonderful day!",
                            color=0xFF5733)

        embed.set_image(url="https://i.redd.it/5lbchzbtl8331.png")

        await message.channel.send('@everyone')
        await message.channel.send(embed=embed)


@tasks.loop(hours=24)
async def test():
    print
    channel = client.get_channel(int(configs.CHANNEL_ID))

    url = base_url + '/check_birthdays'

    r = requests.get(url, headers=headers)

    if r.status_code == 404:
        return

    data = r.json()
    
    if len(data) == 1:
        user = await client.fetch_user(int(data[0]['id']))
        date = datetime.datetime.strptime(data[0]['birthday'],'%Y-%m-%d')
        years = datetime.date.today().year - date.year

        embed = discord.Embed(title=f'Happy Birthday {user.display_name}!',
                        description=f"Today our comrade `{user.display_name}` accomplish `{years} years old`!\nWe wish him/her a wonderful day!",
                        color=0xFF5733)

    else:
        users_data = [await client.fetch_user(int(user_data['id'])) for user_data in data]
        users_names = [user.display_name for user in users_data]
        
        date = datetime.datetime.strptime(data[0]['birthday'],'%Y-%m-%d')
        years = datetime.date.today().year - date.year

        joined_usernames = " and ".join(users_names)
        usernames = joined_usernames.replace(" and ", ", ", len(users_data) - 2)

        embed = discord.Embed(title=f'Happy Birthday {usernames}!',
                        description=f"Today our comrades `{usernames}` accomplish `{years} years old`!\nWe wish them a wonderful day!",
                        color=0xFF5733)

    embed.set_image(url="https://i.redd.it/5lbchzbtl8331.png")

    await channel.send('@everyone')
    await channel.send(embed=embed)




@client.event
async def on_ready():
    test.start()
    

client.run(configs.CLIENT_ID)