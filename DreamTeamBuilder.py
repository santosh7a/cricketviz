import time

start_time = time.time()

import pandas as pd
from sklearn import preprocessing
le = preprocessing.LabelEncoder()

dreamteam = []
dreamteamtotalcost = 0
teamacounter = 0
teambcounter = 0

wkcounter = 0
batcounter = 0
allcounter = 0
bowlcounter = 0

Player = ['Kock', 'warner', 'kpandya', 'jpattinson', 'boult', 'bumrah', 'ssharma', 'ikishan', 'mpandey', 'skaul',
          'hpandya', 'kpollard', 'bairstow', 'rkhan', 'syadav', 'samad', 'rshama', 'asharma', 'M garg', 'chahar',
          'nataraj', 'S williamson']
Role = ['wk', 'bat', 'all', 'bowl', 'bowl', 'bowl', 'bowl', 'wk', 'bat', 'bowl', 'all', 'all', 'wk', 'bowl', 'bat',
        'bat', 'bat', 'all', 'bat', 'bowl', 'bowl', 'bat']
Teams = ['M', 'S', 'M', 'M', 'M', 'M', 'S', 'M', 'S', 'S', 'M', 'M', 'S', 'S', 'M', 'S', 'M', 'S', 'S', 'M', 'S', 'S']
Team=le.fit_transform(Teams)
Team=list(Team)

Cost = [9.5, 10.5,8.5, 8, 8.5, 9, 8, 8.5, 9, 8.5, 9.5, 9, 9.5, 9.5, 9,8, 10.5, 8, 8, 8, 8, 9.5]
Points = [99, 81, 55, 54, 54, 50, 50, 48, 48, 48, 46, 43, 43, 42, 37, 23, 20, 14, 12, 12, 12, 1]

df = pd.DataFrame({'Player': Player, 'Team': Team, 'Role': Role, 'Cost': Cost, 'Points': Points})
df = df.sort_values('Points', ascending=False)

for player, cost, team, role, points in zip(df.Player, df.Cost, df.Team, df.Role, df.Points):
    if (len(dreamteam) < 11) & (teamacounter <= 7) & (teambcounter <= 7) & (wkcounter <= 4) & (batcounter <= 6) & (
            allcounter <= 4) & (bowlcounter <= 6):

        if (team == 0) & (role == 'wk'):
            if wkcounter != 4:
                teamacounter = teamacounter + 1
                wkcounter = wkcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost
        elif (team == 1) & (role == 'wk'):
            if wkcounter != 4:
                teambcounter = teambcounter + 1
                wkcounter = wkcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost

        elif (team == 0) & (role == 'bat'):
            if batcounter != 6:
                teamacounter = teamacounter + 1
                batcounter = batcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost
        elif (team == 1) & (role == 'bat'):
            if batcounter != 6:
                teambcounter = teambcounter + 1
                batcounter = batcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost

        elif (team == 0) & (role == 'all'):
            if allcounter != 4:
                teamacounter = teamacounter + 1
                allcounter = allcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost
        elif (team == 1) & (role == 'all'):
            if allcounter != 4:
                teambcounter = teambcounter + 1
                allcounter = allcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost

        elif (team == 0) & (role == 'bowl'):
            if bowlcounter != 6:
                teamacounter = teamacounter + 1
                bowlcounter = bowlcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost
        elif (team == 1) & (role == 'bowl'):
            if bowlcounter != 6:
                teambcounter = teambcounter + 1
                bowlcounter = bowlcounter + 1
                dreamteam.append([player, cost, team, role, points])
                dreamteamtotalcost = dreamteamtotalcost + cost

        if (len(dreamteam) == 11) & ((wkcounter <= 0) | (batcounter <= 2) | (allcounter <= 0) | (bowlcounter <= 2) | (
                dreamteamtotalcost > 100)):
            if dreamteam[-1][2] == 0:
                teamacounter = teamacounter - 1
            else:
                teambcounter = teambcounter - 1

            if dreamteam[-1][3] == 'wk':
                wkcounter = wkcounter - 1
            elif dreamteam[-1][3] == 'bat':
                batcounter = batcounter - 1
            elif dreamteam[-1][3] == 'all':
                allcounter = allcounter - 1
            elif dreamteam[-1][3] == 'bowl':
                bowlcounter = bowlcounter - 1
            dreamteamtotalcost = dreamteamtotalcost - cost
            del dreamteam[-1]

print(f' Total Players : {len(dreamteam)}')
print(f' Players from TeamA : {teamacounter}')
print(f' Players from TeamB : {teambcounter}')
print(f' No. of Wicket Keepers : {wkcounter}')
print(f' No. of Batsmen : {batcounter}')
print(f' No. of Allrounders : {allcounter}')
print(f' No. of Bowlers : {bowlcounter}')
print(f' Total Cost : {dreamteamtotalcost}')
print(f'Captain is {dreamteam[0][0]}, role {dreamteam[0][3]} of {dreamteam[0][2]} team')
print(f'Vice Captain is {dreamteam[1][0]}, role {dreamteam[1][3]} of {dreamteam[1][2]} team')

dreamteampoints=0
for i in dreamteam:
    dreamteampoints=dreamteampoints + i[4]
print(f'Total points : {dreamteampoints + dreamteam[0][4] + 0.5*dreamteam[1][4] }')
print("Program took", time.time() - start_time, "to run")