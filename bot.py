import discord
import json
import riot.requests_utils as requests
from discord.ext import commands
import asyncio
import os
from utils import w_dir, merge_tags, discord_users, champions, version

client = commands.Bot(command_prefix = '$')

def get_champion(id):
    for champion in champions.values():
        if champion['key'] == id:
            return champion

@client.command()
async def login(ctx, *, arg):

    if str(ctx.author.id) not in discord_users:
        discord_users[str(ctx.author.id)] = {'account_name': arg, 'previous_match': 0}
    else:
        discord_users[str(ctx.author.id)]['account_name'] = arg

    with open(w_dir + '\data\\users.json', 'w') as json_file:
        json.dump(discord_users, json_file)

@client.command()
async def train(ctx):
    account = await requests.get_summoner_info(discord_users[str(ctx.author.id)]['account_name'])
    previous_match_id = await requests.get_previous_match_id(account['accountId'])

    if discord_users[str(ctx.author.id)]['previous_match'] == previous_match_id:
        await ctx.channel.send("You have already trained using your last game.")
    else:
        game_mode, match_data = await requests.get_match_data(previous_match_id, account['accountId'])
        await displayPreviousGame(ctx, game_mode, match_data)
        discord_users[str(ctx.author.id)]['previous_match'] = previous_match_id

        with open(w_dir + '\data\\users.json', 'w') as json_file:
            json.dump(discord_users, json_file)


@client.command()
async def show(ctx, *, arg):
    account = await requests.get_summoner_info(arg)
    previous_match_id = await requests.get_previous_match_id(account['accountId'])
    game_mode, match_data = await requests.get_match_data(previous_match_id, account['accountId'])
    await displayPreviousGame(ctx, game_mode, match_data)


    with open(w_dir + '\data\\users.json', 'w') as json_file:
        json.dump(discord_users, json_file)


@client.command()
async def displayPreviousGame(ctx, game_mode, match_data):
    champion_data = get_champion(str(match_data['championId']))

    embed = discord.Embed(
        title = '{} ({})'.format(champion_data['id'], game_mode),
        description='KDA: {}/{}/{}\nDamage Dealt: {:,}\nDamage Taken: {:,}\nGold Earned: {:,}'.format(
            match_data['stats']['kills'],
            match_data['stats']['deaths'],
            match_data['stats']['assists'],
            match_data['stats']['totalDamageDealtToChampions'],
            match_data['stats']['totalDamageTaken'],
            match_data['stats']['goldEarned'],
        ),
        color=discord.Color.blue()
    )

    champion_img = discord.File(w_dir + '\data\\' + version + '\img\\champion\\' + champion_data['id'] + '.png', filename="image.png")
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=merge_tags(champion_data))
    await ctx.channel.send(file=champion_img,embed=embed)

@client.event
async def on_ready():
    print("Ready")

if __name__ == '__main__':
    client.run('Njg0MjU1NDEwNTcxNTc1Mzk2.Xl3cog.XoB59c0ZkJJhkcuBr9AlO4RA9bY')
