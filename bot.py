import discord
import json
import riot.requests_utils as requests
from discord.ext import commands
import asyncio
import os
import copy
import typing

from utils import (
    discord_users,
    update_discord_users,
    generate_new_user_champion,
    update_user_champion,
    displayPreviousGame,
    displayChampion,
    get_user_champion,
    attack,
    import_key
)

client = commands.Bot(command_prefix = '$')

#TODO: if champions don't exist show error
@client.command()
async def battle(ctx, opponent: discord.Member, champ1, champ2):
    my_champ = copy.deepcopy(get_user_champion(ctx.author.id, champ1))
    my_champ['owner'] = ctx.author.display_name
    my_champ['champ']= champ1

    opp_champ = copy.deepcopy(get_user_champion(opponent.id, champ2))
    opp_champ['owner'] = opponent.display_name
    opp_champ['champ'] = champ2

    if my_champ['spd'] >= opp_champ['spd']:
        turn_order = [my_champ, opp_champ]
    else:
        turn_order = [opp_champ, my_champ]

    turn = 0
    attacker = 0
    defender = 1
    while my_champ['hp'] > 0 and opp_champ['hp'] > 0 and turn < 20:
        await attack(ctx, turn_order, attacker, defender)
        turn += 1
        attacker, defender = defender, attacker
        await asyncio.sleep(1)

    if my_champ['hp'] < 0:
        await ctx.send("{}'s {} wins!".format(opp_champ['owner'] , opp_champ['champ']))
    elif opp_champ['hp'] < 0:
        await ctx.send("{}'s {} wins!".format(my_champ['owner'] , my_champ['champ']))
    else:
        await ctx.send("The two champions are too tired to continue. It's a draw!")

@client.command()
async def login(ctx, *, arg):

    if str(ctx.author.id) not in discord_users:
        discord_users[str(ctx.author.id)] = {'account_name': arg, 'previous_match': 0, 'champions': {}}
    else:
        discord_users[str(ctx.author.id)]['account_name'] = arg

    #try:
        update_discord_users()
    await ctx.send("Logged in as {}".format(arg))
    #catch:


@client.command()
async def train(ctx):
    author_id = str(ctx.author.id)

    if author_id not in discord_users:
        return

    account = await requests.get_summoner_info(discord_users[author_id]['account_name'])
    previous_match_id = await requests.get_previous_match_id(account['accountId'])

    if discord_users[author_id]['previous_match'] == previous_match_id:
        await ctx.channel.send("You have already trained using your last game.")
    else:
        game_mode, match_data = await requests.get_match_data(previous_match_id, account['accountId'])
        await displayPreviousGame(ctx, game_mode, match_data)

        champion_id = str(match_data['championId'])

        if champion_id not in discord_users[author_id]['champions']:
            generate_new_user_champion(author_id, champion_id)

        update_user_champion(match_data, author_id, champion_id)

        discord_users[author_id]['previous_match'] = previous_match_id

        update_discord_users()

@client.command()
async def showchamp(ctx, member: typing.Optional[discord.Member], champion_name):
    if member == None:
        await displayChampion(ctx, ctx.author.id, champion_name)
    else:
        await displayChampion(ctx, member.id, champion_name)


@client.command()
async def show(ctx, *, arg):
    account = await requests.get_summoner_info(arg)
    previous_match_id = await requests.get_previous_match_id(account['accountId'])
    game_mode, match_data = await requests.get_match_data(previous_match_id, account['accountId'])
    await displayPreviousGame(ctx, game_mode, match_data)



@client.event
async def on_ready():
    print("Ready")

if __name__ == '__main__':
    client.run(import_key())
