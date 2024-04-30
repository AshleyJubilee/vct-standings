import requests
import pandas as pd
import uvicorn

# uvicorn.run("main:app", port=5000, log_level="info")

amerID = []
cnID = []
pacID = []
emeaID = []
amerMap = []
cnMap = []
pacMap = []
emeaMap = []


# Stage 1 Region ID's
regions = [
    ('amerReg', amerID, amerMap, '2004'), 
    ('cnReg', cnID, cnMap, '2006'), 
    ('pacReg', pacID, pacMap, '2002'), 
    ('emeaReg', emeaID, emeaMap, '1998')]


url = "http://127.0.0.1:8000"

def vlrAPI(endpoint, param=None):
    response = requests.get(f'{url}/{endpoint}/{param}').json()
    return response

# Get All Match ID's for event
for region in regions:
    for day in vlrAPI('event', region[3])['matches']:
        for match in day['matches']:
            region[1].append(
                {'id': match['id'],
                 'stage': match['stage']})
    print(f'{region[0]} ID\'s Retrived')
            
# Get Regular Season Results for each match
for region in regions:
    for match in region[1]:
        try: 
            if match['stage'] == 'Regular Season':

                response = vlrAPI('match', match['id'])
                matchID = match['id']
                score = response['score']

                for map in response['data']:
                    if map['map'] != 'All Maps': 

                        mapName = map['map']
                        teamA = map['teams'][0]['name']
                        teamAScore = map['teams'][0]['score']
                        teamB = map['teams'][1]['name']
                        teamBScore = map['teams'][1]['score']

                        region[2].append({
                            'id': matchID,
                            'matchResult': score,
                            'map': mapName,
                            'teamA': teamA,
                            'teamAScore': teamAScore,
                            'teamB': teamB,
                            'teamBScore': teamBScore,
                        })
        except: 
            print('missing')
    print(f'{region[0]} Map\'s Retrived')


# To CSV
for region in regions:
    df = pd.DataFrame(region[2])
    df.to_csv(f'resources/{region[0]}.csv', index=False)
