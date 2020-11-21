import numpy as np
import pandas as pd
import datetime
import yaml
import os

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 25)

# update this directory as necessary
os.chdir(r"ipl")

# Uncomment only when you want to update files
filenames = []
yamlipl = []

for i in os.listdir():
    with open(i, 'r') as file:
        filenames.append(str(i))
        yamlipl.append(yaml.load(file, Loader=yaml.FullLoader))

sanmatchesraw = pd.DataFrame()
for match in yamlipl:
    sanmatchesraw = sanmatchesraw.append(pd.json_normalize(match['info']))

sanmatchesraw.reset_index(inplace=True)
sanmatchesraw.drop(['index', 'competition', 'gender', 'match_type', 'overs',
                    'neutral_venue', 'umpires'], axis=1, inplace=True)
sanmatchesraw = sanmatchesraw[['dates', 'city', 'venue', 'teams', 'toss.winner',
                               'toss.decision', 'outcome.winner',
                               'outcome.by.runs', 'outcome.by.wickets', 'player_of_match',
                               'outcome.eliminator', 'outcome.result', 'outcome.method']]

ldates = []
for lists in sanmatchesraw['dates']:
    if len(lists) == 1:
        for dates in lists:
            if isinstance(dates, str):
                ldates.append(
                    datetime.date(int(dates.split('-')[0]), int(dates.split('-')[1]), int(dates.split('-')[2])))
            else:
                ldates.append(dates)
    else:
        if isinstance(lists[0], str):
            ldates.append(datetime.date(int(lists[0].split('-')[0]), int(lists[0].split('-')[1]), int(lists[0].split('-')[2])))
        else:
            ldates.append(lists[0])

# the following spoonfed corrections will be deleted if above date checking block works out
# sanmatchesraw.loc[4,'dates']  =[[datetime.date(2017, 4,  8)]]
# sanmatchesraw.loc[56,'dates'] =[[datetime.date(2017, 5, 17)]]
# sanmatchesraw.loc[241,'dates']=[[datetime.date(2008, 4, 19)]]
# sanmatchesraw.loc[499,'dates']=[[datetime.date(2012, 4, 12)]]
# sanmatchesraw.loc[693,'dates']=[[datetime.date(2014, 5, 28)]]

# list1=[]
# for row in sanmatchesraw.loc[59:238,'dates']:
#    for entry in row:
#        list1.append(entry)
# list2=pd.Series(list1).apply(pd.to_datetime)
# list3=[]
# for i in list2:
#    list3.append(i.date())

# sanmatchesraw['date']=sanmatchesraw['dates']
# sanmatchesraw.loc[59:238,'date']=list3

# list4=[]
# for row in sanmatchesraw.loc[0:58,'date']:
#    for element in row:
#        list4.append(element)

# for row in sanmatchesraw.loc[59:238,'date']:
#    list4.append(row)

# for row in sanmatchesraw.loc[239:815,'date']:
#    for element in row:
#        list4.append(element)

# sanmatchesraw['date']=list4


sanmatchesraw['date'] = ldates

sanmatchesraw.drop('dates', axis=1, inplace=True)

sanmatchesraw = sanmatchesraw[['date', 'city', 'venue', 'teams', 'toss.winner', 'toss.decision',
                               'outcome.winner', 'outcome.by.runs', 'outcome.by.wickets',
                               'player_of_match', 'outcome.eliminator', 'outcome.result',
                               'outcome.method']]

sanmatchesraw['date'] = pd.to_datetime(sanmatchesraw['date'])

season = []
for row in sanmatchesraw['date']:
    season.append(row.year)

sanmatchesraw['season'] = season

sanmatchesraw = sanmatchesraw[['season', 'date', 'city', 'venue', 'teams', 'toss.winner',
                               'toss.decision', 'outcome.winner', 'outcome.by.runs',
                               'outcome.by.wickets', 'player_of_match', 'outcome.eliminator',
                               'outcome.result', 'outcome.method']]

sanmatchesraw = sanmatchesraw.replace('tie', 'superover')

sanmatchesraw.loc[sanmatchesraw['outcome.eliminator'].notna(), 'outcome.winner'] = sanmatchesraw.loc[
    sanmatchesraw['outcome.eliminator'].notna(), 'outcome.eliminator']

match_id = np.arange(len(sanmatchesraw['season']))
match_id = pd.Series(match_id)

sanmatches = pd.concat([match_id, sanmatchesraw], axis=1)

sanmatches = sanmatches.rename(
    columns={0: 'match_id', 'toss.winner': 'toss_winner', 'toss.decision': 'toss_decision', 'outcome.winner': 'winner',
             'outcome.by.runs': 'win_by_runs', 'outcome.by.wickets': 'win_by_wickets', 'outcome.result': 'result',
             'outcome.method': 'method'})

sanmatches.drop('outcome.eliminator', axis=1, inplace=True)

sanmatches['result'] = sanmatches['result'].fillna(0)
sanmatches['method'] = sanmatches['method'].fillna(0)

sanmatches = sanmatches.sort_values('date')
sanmatches.reset_index(inplace=True)
sanmatches.drop('index', axis=1, inplace=True)

team_1 = []
team_2 = []
for i in sanmatches['teams']:
    team_1.append(i[0])
    team_2.append(i[1])

team_1 = pd.Series(team_1)
team_2 = pd.Series(team_2)

sanmatches = pd.concat([team_1, sanmatches], axis=1)
sanmatches = sanmatches.rename(columns={0: "team_1"})

sanmatches = pd.concat([team_2, sanmatches], axis=1)
sanmatches = sanmatches.rename(columns={0: "team_2"})

sanmatches = sanmatches[['match_id',
                         'season', 'date', 'city',
                         'venue', 'teams', 'team_1', 'team_2', 'toss_winner',
                         'toss_decision', 'winner', 'win_by_runs',
                         'win_by_wickets', 'player_of_match', 'result',
                         'method']]

sanmatches.replace(
    ['Mumbai Indians', 'Kolkata Knight Riders', 'Royal Challengers Bangalore', 'Deccan Chargers', 'Chennai Super Kings',
     'Rajasthan Royals', 'Delhi Daredevils', 'Gujarat Lions', 'Kings XI Punjab',
     'Sunrisers Hyderabad', 'Rising Pune Supergiants', 'Kochi Tuskers Kerala',
     'Pune Warriors', 'Rising Pune Supergiant']
    , ['MI', 'KKR', 'RCB', 'DC', 'CSK', 'RR', 'DD', 'GL', 'KXIP', 'SRH', 'RPS', 'KTK', 'PW', 'RPS'], inplace=True)
sanmatches.replace(['DC'], ['SRH'], inplace=True)
sanmatches.replace(['DD'], ['DC'], inplace=True)
sanmatches.replace(['Delhi Capitals'], ['DC', ], inplace=True)

# uncomment WHEN NECESSARY
os.chdir(r"C:\Users\santosh\PycharmProjects\Cricket")
sanmatches.to_csv('IPL_matches.csv', index=False)
