import discord
import json
import riot.requests_utils as requests
from discord.ext import commands
import asyncio
import os

version = '10.9.1'

w_dir = os.getcwd()

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

with open(w_dir + '\data\\' + version + '\champion.json', encoding="utf8") as f:
    champions = json.load(f)
    champions = champions['data']

status = ['Hi', 'Sup', 'Bye']


def get_champion(id):
    for champion in champions.values():
        if champion['key'] == id:
            return champion


@client.command()
async def train(ctx, *, arg):
    account = await requests.get_summoner_info(arg)
    previous_match_id = await requests.get_previous_match_id(account['accountId'])
    game_mode, match_data = await requests.get_match_data(previous_match_id, account['accountId'])
    await displayPreviousGame(ctx, game_mode, match_data)


@client.command()
async def displayPreviousGame(ctx, game_mode, match_data):
    champion_data = get_champion(str(match_data['championId']))

    embed = discord.Embed(
        title = '{} ({})'.format(champion_data['id'], game_mode),
        description='KDA: {}/{}/{}'.format(match_data['stats']['kills'], match_data['stats']['deaths'], match_data['stats']['assists']),
        color=discord.Color.blue()
    )

    embed.set_footer(text="ADC")
    embed.set_image(url='https://gamepedia.cursecdn.com/lolesports_gamepedia_en/1/1e/LucianSquare.png')
    await ctx.channel.send(embed=embed)

@client.event
async def on_ready():
    print("Ready")

client.run('Njg0MjU1NDEwNTcxNTc1Mzk2.Xl3cog.XoB59c0ZkJJhkcuBr9AlO4RA9bY')
