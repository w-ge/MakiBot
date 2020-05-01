import discord
import json
import riot.requests_utils as requests
from discord.ext import commands
import asyncio


client = commands.Bot(command_prefix = '$')
client.remove_command('help')

status = ['Hi', 'Sup', 'Bye']

@client.command()
async def train(ctx, *, arg):
    account = await requests.get_summoner_info(arg)
    previous_match_id = await requests.get_previous_match_id(account['accountId'])
    match_data = await requests.get_match_data(previous_match_id, account['accountId'])
    print('{}/{}/{}'.format(match_data['stats']['kills'], match_data['stats']['deaths'], match_data['stats']['assists']))


@client.command()
async def displayPreviousGame(ctx):
    embed = discord.Embed(
        title = 'Lucian',
        description='Gunslinger',
        color=discord.Color.blue()
    )

    embed.set_footer(text="ADC")
    embed.set_image(url='https://gamepedia.cursecdn.com/lolesports_gamepedia_en/1/1e/LucianSquare.png')
    await ctx.channel.send(embed=embed)

@client.event
async def on_ready():
    print("Ready")

client.run('Njg0MjU1NDEwNTcxNTc1Mzk2.Xl3cog.XoB59c0ZkJJhkcuBr9AlO4RA9bY')
