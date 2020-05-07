import os
import json

version = '10.9.1'
w_dir = os.getcwd()

with open(w_dir + '\data\\users.json') as f:
    discord_users = json.load(f)

with open(w_dir + '\data\\' + version + '\champion.json', encoding="utf8") as f:
    champions = json.load(f)
    champions = champions['data']

def merge_tags(champion_data):
    tags = ""
    for tag in champion_data['tags']:
        tags = tags + tag + ", "
    tags = tags[:-2]
    return tags

def update_discord_users():
    with open(w_dir + '\data\\users.json', 'w') as json_file:
        json.dump(discord_users, json_file)