import pandas as pd
import numpy as np

amerMaps = pd.read_csv('resources/amerRegMaps.csv')
cnMaps = pd.read_csv('resources/cnRegMaps.csv')
pacMaps = pd.read_csv('resources/pacRegMaps.csv')
emeaMaps = pd.read_csv('resources/emeaRegMaps.csv')

regions = {'amer': amerMaps, 'cn': cnMaps, 'pac': pacMaps, 'emea': emeaMaps}

for region in regions.keys(): 

    # Rounds per Team
    rounds = pd.concat(
        [regions[region].groupby(['teamA']).sum(['teamAScore', 'teamBScore']).rename(columns={'teamAScore': 'Round Wins', 'teamBScore': 'Round Losses'}),
        regions[region].groupby(['teamB']).sum(['teamBScore', 'teamAScore']).rename(columns={'teamBScore': 'Round Wins', 'teamAScore': 'Round Losses'})]
            ).groupby(level=0).sum()
    
    rounds['Round Delta'] = rounds['Round Wins'] - rounds['Round Losses']

    # Maps per Team
    maps = pd.concat(
        [regions[region].groupby(['teamA']).value_counts(['teamAResult']).unstack(), 
        regions[region].groupby(['teamB']).value_counts(['teamBResult']).unstack()])

    maps = maps.groupby(level=0).sum().rename(columns={'W': 'Map Wins', 'L': 'Map Losses'})
    maps['Map Delta'] = maps['Map Wins'] - maps['Map Losses']    
    
    # Team Record
    record = pd.DataFrame({'Wins': regions[region].groupby('matchWinner')['id'].nunique(),
                            'Losses': regions[region].groupby('matchLoser')['id'].nunique()}).fillna(0)
    
    teams = pd.merge(record, maps, left_index=True, right_index=True).merge(rounds, left_index=True, right_index=True).astype(int)
    teams.insert(2, 'Map Wins', teams.pop('Map Wins'))

    teams.to_csv(f'resources/{region}Teams.csv')