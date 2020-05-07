import requests

headers = {'X-Riot-Token': 'RGAPI-ec0baa62-dbf9-4bea-a9ff-83e356ab6a06'}

async def get_summoner_info(summoner_name):
    r = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name, headers = headers)
    return r.json()

async def get_previous_match_id(account):
    params = {'endIndex': 1, 'beginIndex': 0}
    r = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account, params = params, headers = headers)
    r = r.json()
    match = r['matches'][0]
    return match['gameId']

async def get_match_data(match_id, account_id):
    r = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' + str(match_id), headers = headers)
    r = r.json()

    game_mode = r['gameMode']
    participants = r['participants']
    participant_identities = r['participantIdentities']
    participant_id = find_participant_id(participant_identities, account_id)
    return  game_mode, participants[participant_id - 1]

def find_participant_id(participantIdentities, account_id):
    for participant in participantIdentities:
        if participant['player']['accountId'] == account_id:
            return  int(participant['participantId'])
