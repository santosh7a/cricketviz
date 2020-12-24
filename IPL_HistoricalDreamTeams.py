# will later add player roles to get much deeper insights

import os
os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')

import numpy as np
import pandas as pd
pd.set_option('display.max_columns',40)
pd.set_option('display.max_rows',1000)

matches = pd.read_csv('IPL_matches.csv')
deliveries_including_superovers = pd.read_csv('IPL_deliveries.csv')

deliveries = deliveries_including_superovers[(deliveries_including_superovers['innings'] == '1st innings') | (deliveries_including_superovers['innings'] == '2nd innings')]
md = matches.merge(deliveries)

batsmanscores = md.groupby(['season', 'match_id', 'striker'], sort=False).agg(np.sum)
batsmanscores = batsmanscores[['batsman_runs']]
batsmanscores.reset_index(inplace=True)
batsmanscores.rename(columns={'striker': 'player'}, inplace=True)

bowlerprep = md[(md['kind_of_dismissal'] != 'run out') & (md['kind_of_dismissal'] != 'retired hurt') & (md['kind_of_dismissal'] != 'obstructing the field')]
bowlerscores = bowlerprep.groupby(['season', 'match_id', 'bowler'], sort=False).agg(np.sum)
bowlerscores = bowlerscores[['wicket']]
bowlerscores.reset_index(inplace=True)
bowlerscores.rename(columns={'bowler': 'player'}, inplace=True)

fielderprep = md.copy()
#"Caught and bowled" wicket deliveries have fielder column empty which must have the value of bowler himself
fielderprep['fielders'] = np.where(fielderprep['kind_of_dismissal']=='caught and bowled', fielderprep['bowler'], fielderprep['fielders'])

fielderprep = fielderprep.groupby(['season', 'match_id', 'bowler', 'kind_of_dismissal', 'fielders']).agg(np.sum)
fielderprep.reset_index(inplace =True)
fielderprep = fielderprep.drop(['win_by_runs', 'win_by_wickets', 'delivery', 'wides', 'legbyes',
       'noballs', 'byes', 'penalty', 'non_boundary', 'batsman_runs',
       'extra_runs', 'total_runs', 'wicket'], axis=1)
fielderprep['fielders'] = fielderprep['fielders'].str.replace('[','').str.replace(']','').str.replace("'","")

fielderprep.drop('bowler', axis =1, inplace = True)
fielderprep.rename(columns={'fielders':'player'}, inplace=True)

# There are no points for substitutes, let's remove those rows.
for i, j in zip(fielderprep.index, fielderprep['player']):
    if '(sub)' in j:
        fielderprep.drop(i, inplace=True)

        fielderprep['fielding_points'] = np.where(fielderprep['kind_of_dismissal']=='caught', 8, 0)
fielderprep['fielding_points'] = np.where(fielderprep['kind_of_dismissal']=='caught and bowled', 8, fielderprep['fielding_points'])
fielderprep['fielding_points'] = np.where(fielderprep['kind_of_dismissal']=='stumped', 12, fielderprep['fielding_points'])

# assigning points for direct hits
condition = (fielderprep['kind_of_dismissal']=='run out') & (fielderprep['player'].str.split(',').str.len()==1)
fielderprep['fielding_points'] = np.where(condition, 12, fielderprep['fielding_points'])

# assigning points for non-direct hits
fielderprep = fielderprep.assign(player=fielderprep['player'].str.split(',')).explode('player')
fielderprep['fielding_points'] = np.where(fielderprep['fielding_points']==0,6,fielderprep['fielding_points'])
fieldingscores = fielderprep.groupby(['season', 'match_id', 'player']).agg(np.sum).reset_index()
fieldingscores['player'] = fieldingscores['player'].str.strip()
matchteam_bb = batsmanscores.merge(bowlerscores, left_on=['season', 'match_id', 'player'], right_on=['season', 'match_id', 'player'], how='outer')

matchteam_bb.rename(columns={'batsman_runs': 'player_runs', 'wicket': 'player_wickets'}, inplace=True)
matchteam_bb.fillna(0, inplace=True)
matchteam = matchteam_bb.merge(fieldingscores,  left_on=['season', 'match_id', 'player'], right_on=['season', 'match_id', 'player'], how='outer')
matchteam.fillna(0, inplace=True)

# making points columns
matchteam['runs_points'] = np.where((matchteam['player_runs'] >= 50) & (matchteam['player_runs'] < 100), matchteam['player_runs']+8, matchteam['player_runs'])
matchteam['runs_points'] = np.where(matchteam['player_runs'] >= 100, matchteam['player_runs']+16, matchteam['runs_points'])
matchteam['runs_points'] = np.where(matchteam['player_runs'] == 0, -2, matchteam['runs_points'])

matchteam['bowling_points'] = np.where(matchteam['player_wickets'] >= 4, (matchteam['player_wickets']*25)+16, matchteam['player_wickets']*25)

matchteam['total_points'] = matchteam['runs_points'] + matchteam['bowling_points'] + matchteam['fielding_points']

# dreamteams for matches
season_list = []
match_num = []
player_name = []
run_points = []
bowl_points = []
field_points = []
player_points = []

# I tried sorting, that messes up the grouped matches, so now we take in each match and then sort.
# Then we append top 11 players and their points to lists.

for i in matchteam['match_id'].unique():
    tempdf = matchteam[matchteam['match_id'] == i]
    topelevendf = tempdf.nlargest(11, 'total_points')
    for j in list(topelevendf['match_id']):
        match_num.append(j)
    for k in list(topelevendf['player']):
        player_name.append(k)
    for l in list(topelevendf['total_points']):
        player_points.append(l)
    for m in list(topelevendf['season']):
        season_list.append(m)
    for n in list(topelevendf['runs_points']):
        run_points.append(n)
    for o in list(topelevendf['bowling_points']):
        bowl_points.append(o)
    for p in list(topelevendf['fielding_points']):
        field_points.append(p)
dreamteamdf = pd.DataFrame({'season': season_list, 'match_id': match_num, 'player': player_name,
                            'runs_points': run_points,'bowling_points': bowl_points, 'fielding_points': field_points,
                            'total_points': player_points})

# using IPL_Players dataset to add a column of DOB for matchteam
os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')
ipl_players = pd.read_csv('IPL_Players.csv')
ipl_players.drop(['Age', 'Teams', 'Matches', 'Runs', 'Bat avg', 'Wickets',
                  'Bowl avg', 'PlayerID'], axis=1, inplace=True)
ipl_players.rename(columns={'Name': 'player'}, inplace=True)
ipl_players['DOB'] = pd.to_datetime(ipl_players['DOB'])

matchteammergedf = matchteam.merge(ipl_players, how='outer', left_on='player', right_on='player')
matchteammergedf = matchteammergedf.loc[0:17650, :]  # removing a few NA rows at the bottom arising out of merging
matchteammergedf['season'] = pd.to_datetime(matchteammergedf['season'], format='%Y')
matchteammergedf['matchday_player_age'] = (matchteammergedf['season'] - matchteammergedf['DOB']).astype('<m8[Y]')
# Just accomplished a cool thing, we have age as on match day for all players for all matches

# using IPL_Players dataset to add a column of DOB for dreamteamdf too

dreamteamdfmerge = dreamteamdf.merge(ipl_players, how='inner')
dreamteamdfmerge['season'] = pd.to_datetime(dreamteamdfmerge['season'], format='%Y')
dreamteamdfmerge['matchday_player_age'] = (dreamteamdfmerge['season'] - dreamteamdfmerge['DOB']).astype('<m8[Y]')

os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')
matchteammergedf.to_csv('IPL_matchwise_player_points.csv', index=False)

os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')
dreamteamdfmerge.to_csv('IPL_historical_dreamteams.csv', index=False)
