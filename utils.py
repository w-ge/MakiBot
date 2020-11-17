import os
import json
import discord
import math
import asyncio
import random

version = '10.9.1'
w_dir = os.getcwd()
base_hp = 0
base_atk =  0
base_def = 0
base_speed =  0
hp_modifier = 0.001
atk_modifier = 0.0001
def_modifier = 0.0001
spd_modifier = 0.0001
kda_modifier = 1
minimum_damage=2
lck_damage_min = 0
lck_damage_max = 10

with open(w_dir + '\data\\users.json') as f:
    discord_users = json.load(f)

with open(w_dir + '\data\\' + version + '\champion.json', encoding="utf8") as f:
    champions = json.load(f)
    champions = champions['data']

def import_key():
    return os.getenv("BOT_KEY")


async def attack(ctx, turn_order, attacker, defender):
    damage = max(turn_order[attacker]['atk'] - turn_order[defender]['def'], minimum_damage) + random.randint(lck_damage_min, lck_damage_max)
    turn_order[defender]['hp'] -= damage
    await ctx.send("{}'s {} deals {} damage to {}'s {}. {} has {} hp left".format(
        turn_order[attacker]['owner'],
        turn_order[attacker]['champ'],
        damage,
        turn_order[defender]['owner'],
        turn_order[defender]['champ'],
        turn_order[defender]['champ'],
        turn_order[defender]['hp']
    ))

def merge_tags(champion_data):
    tags = ""
    for tag in champion_data['tags']:
        tags = tags + tag + ", "
    tags = tags[:-2]
    return tags

def update_discord_users():
    with open(w_dir + '\data\\users.json', 'w') as json_file:
        json.dump(discord_users, json_file)

def get_champion(match_data):
    id = str(match_data['championId'])
    for champion in champions.values():
        if champion['key'] == id:
            return champion

def get_user_champion(user_id, champion_name):
    champion_data = get_champion_by_name(champion_name)

    return discord_users[str(user_id)]['champions'][champion_data['key']]


def get_champion_by_name(champion_name):
    for champion in champions.values():
        if champion['id'] == champion_name:
            return champion
    return None

def generate_new_user_champion(author_id, champion_id):
    discord_users[author_id]['champions'][champion_id] = {'hp': base_hp, 'atk': base_atk, 'def': base_def, 'spd': base_speed}

def update_user_champion(match_data, author_id, champion_id):
    kda = round((match_data['stats']['kills'] + match_data['stats']['assists']) / match_data['stats']['deaths']) * kda_modifier
    discord_users[author_id]['champions'][champion_id]['hp'] += kda + round(match_data['stats']['totalDamageTaken'] * hp_modifier)
    discord_users[author_id]['champions'][champion_id]['atk'] += kda + round(match_data['stats']['totalDamageDealtToChampions'] * atk_modifier)
    discord_users[author_id]['champions'][champion_id]['def'] += kda + round(match_data['stats']['damageSelfMitigated'] * atk_modifier)
    discord_users[author_id]['champions'][champion_id]['spd'] += kda + round(match_data['stats']['goldEarned'] * spd_modifier)
    

async def displayPreviousGame(ctx, game_mode, match_data):
    champion_data = get_champion(match_data)

    embed = discord.Embed(
        title = '{} ({})'.format(champion_data['id'], game_mode),
        description='KDA: {}/{}/{}\nDamage Dealt: {:,}\nDamage Taken: {:,}\nGold Earned: {:,}\nDamage Mitigated: {:,}'.format(
            match_data['stats']['kills'],
            match_data['stats']['deaths'],
            match_data['stats']['assists'],
            match_data['stats']['totalDamageDealtToChampions'],
            match_data['stats']['totalDamageTaken'],
            match_data['stats']['goldEarned'],
            match_data['stats']['damageSelfMitigated']
        ),
        color=discord.Color.blue()
    )

    champion_img = discord.File(w_dir + '\data\\' + version + '\img\\champion\\' + champion_data['id'] + '.png', filename="image.png")
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=merge_tags(champion_data))
    await ctx.channel.send(file=champion_img,embed=embed)

async def displayChampion(ctx, author_id, champion_name):
    champion_data = get_champion_by_name(champion_name)

    if not champion_data:
        return

    user_champion = discord_users[str(author_id)]['champions'][champion_data['key']]
    embed = discord.Embed(
        title = '{}'.format(champion_name),
        description='HP: {:,}\nATK: {:,}\nDEF: {:,}\nSPD: {:,}\n'.format(
            user_champion['hp'],
            user_champion['atk'],
            user_champion['def'],
            user_champion['spd'],
        ),
        color=discord.Color.blue()
    )

    champion_img = discord.File(w_dir + '\data\\' + version + '\img\\champion\\' + champion_name + '.png', filename="image.png")
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=merge_tags(champion_data))
    await ctx.channel.send(file=champion_img, embed=embed)

