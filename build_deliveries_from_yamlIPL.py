import numpy as np
import pandas as pd
import yaml
import os

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 25)

os.chdir(r"ipl")

yamldeliveries = []
filenames = []

for file in os.listdir():
    with open(file, 'r') as f:
        filenames.append(str(file))
        yamldeliveries.append(yaml.load(f, Loader=yaml.FullLoader))

listofdeliveries = []
battingteam = []
teams = []
matchinning = []
match_id = []
matchid = 0

for match in yamldeliveries:
    for inning in match['innings']:
        for firstsecond in inning:
            for deliveryrow in inning[firstsecond]['deliveries']:
                listofdeliveries.append(deliveryrow)
                battingteam.append(inning[firstsecond]['team'])
                teams.append(match['info']['teams'])
                matchinning.append(firstsecond)
                match_id.append(matchid)
    matchid = matchid + 1

keys = []
for dictionaries in listofdeliveries:
    for key in dictionaries.keys():
        keys.append(key)

values = []
for dictionaries in listofdeliveries:
    for value in dictionaries.values():
        values.append(value)
team_1 = []
team_2 = []
for row in teams:
    team_1.append(row[0])
    team_2.append(row[1])

match_id = pd.Series(match_id)
matchinning = pd.Series(matchinning)
team_1 = pd.Series(team_1)
team_2 = pd.Series(team_2)
keys = pd.Series(keys)
battingteam = pd.Series(battingteam)

valuesdf = pd.DataFrame(values)

valuesdf.rename(columns={'batsman': 'striker'}, inplace=True)

valuesdf['extras'] = valuesdf['extras'].apply(lambda x: {} if pd.isna(x) else x)
valuesdf['wicket'] = valuesdf['wicket'].apply(lambda x: {} if pd.isna(x) else x)

tempruns = pd.json_normalize(valuesdf['runs'])
tempextras = pd.json_normalize(valuesdf['extras'])
tempwickets = pd.json_normalize(valuesdf['wicket'])

innings = pd.concat([match_id, matchinning, team_1, team_2, battingteam, keys, valuesdf, tempextras, tempruns,
                     tempwickets], axis=1)

innings = innings.rename(columns={0: 'match_id', 1: 'innings', 2: 'team_1', 3: 'team_2', 4: 'batting_team',
                                  5: 'delivery', 'batsman': 'batsman_runs', 'total': 'total_runs',
                                  'kind': 'kind_of_dismissal'})
innings.drop(['extras', 'runs', 'wicket'], axis=1, inplace=True)

innings['bowling_team'] = np.where(innings['team_1'] == innings['batting_team'], innings['team_2'], innings['team_1'])

innings = innings[['match_id', 'innings', 'team_1', 'team_2', 'batting_team', 'bowling_team', 'delivery', 'striker',
                   'bowler', 'non_striker', 'wides', 'legbyes', 'noballs', 'byes', 'penalty', 'batsman_runs',
                   'total_runs', 'non_boundary', 'fielders', 'kind_of_dismissal', 'player_out']]

innings.drop(['team_1', 'team_2'], axis=1, inplace=True)

innings.loc[:, 'legbyes'].fillna(0, inplace=True)
innings.loc[:, 'wides'].fillna(0, inplace=True)
innings.loc[:, 'byes'].fillna(0, inplace=True)
innings.loc[:, 'noballs'].fillna(0, inplace=True)
innings.loc[:, 'penalty'].fillna(0, inplace=True)
innings.loc[:, 'non_boundary'].fillna(0, inplace=True)
innings['extra_runs'] = innings['legbyes'] + innings['wides'] + innings['byes'] + innings['noballs'] + innings[
    'penalty']

innings = innings[['match_id', 'innings', 'batting_team', 'bowling_team', 'delivery', 'striker',
                   'bowler', 'non_striker', 'wides', 'legbyes', 'noballs', 'byes', 'penalty', 'non_boundary',
                   'batsman_runs', 'extra_runs', 'total_runs', 'fielders', 'kind_of_dismissal', 'player_out']]

innings.replace(['Mumbai Indians', 'Kolkata Knight Riders', 'Royal Challengers Bangalore', 'Deccan Chargers',
                 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Daredevils', 'Gujarat Lions', 'Kings XI Punjab',
                 'Sunrisers Hyderabad', 'Rising Pune Supergiants', 'Kochi Tuskers Kerala', 'Pune Warriors',
                 'Rising Pune Supergiant'], ['MI', 'KKR', 'RCB', 'DC', 'CSK', 'RR', 'DD', 'GL', 'KXIP', 'SRH',
                                             'RPS', 'KTK', 'PW', 'RPS'], inplace=True)
innings.replace(['DC'], ['SRH'], inplace=True)
innings.replace(['DD'], ['DC'], inplace=True)
innings.replace(['Delhi Capitals'], ['DC'], inplace=True)

innings['wicket'] = np.where(innings['kind_of_dismissal'].notna(), 1, 0)
innings = innings[['match_id', 'innings', 'batting_team', 'bowling_team', 'delivery',
                   'striker', 'bowler', 'non_striker', 'wides', 'legbyes', 'noballs',
                   'byes', 'penalty', 'non_boundary', 'batsman_runs', 'extra_runs',
                   'total_runs', 'wicket', 'player_out', 'kind_of_dismissal', 'fielders']]

# UNCOMMENT WHEN NECESSARY
os.chdir(r"C:\Users\santosh\PycharmProjects\Cricket")
innings.to_csv('IPL_deliveries.csv', index=False)