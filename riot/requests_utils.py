import requests

headers = {'X-Riot-Token': 'RGAPI-24004a94-55e4-4beb-8ad6-b3e3ee59b640'}

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
    participants = r['participants']
    participantIdentities = r['participantIdentities']
    participant_id = find_participant_id(participantIdentities, account_id)
    return  participants[participant_id - 1]



def find_participant_id(participantIdentities, account_id):
    for participant in participantIdentities:
        if participant['player']['accountId'] == account_id:
            return  int(participant['participantId'])
