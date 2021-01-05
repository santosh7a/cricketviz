# Importing necessary libraries
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# import os
st.header('A brief Visual Journey into the Cricketing World of **IPL**')
# sns.set_style(style='darkgrid')
# sns.set_context("talk")
#
# # os.chdir(r'C:\Users\santosh\PycharmProjects\Cricket')
#
# # Importing the datasets
# matches = pd.read_csv('IPL_matches.csv')
# deliveries_including_superovers = pd.read_csv('IPL_deliveries.csv')
# deliveries = deliveries_including_superovers[(deliveries_including_superovers['innings'] == '1st innings')
#                                              | (deliveries_including_superovers['innings'] == '2nd innings')]
# match_points = pd.read_csv('IPL_matchwise_player_points.csv')
# dreamteams = pd.read_csv('IPL_historical_dreamteams.csv')
#
# # Building a dataframe to get innings total runs and wickets i.e score cards
# matchscores = deliveries.groupby(['match_id', 'innings', 'batting_team', 'bowling_team']).agg(np.sum)
# matchscores = matchscores.reset_index().drop(['delivery', 'wides', 'legbyes', 'noballs', 'byes', 'penalty',
#                                               'non_boundary'], axis=1)
#
# # Building a dataframe to get individual scores of players
# batsmanlistofscores = matches.merge(deliveries, how='outer').groupby(['striker', 'match_id', 'season'],
#                                                                      sort=False).agg(np.sum).reset_index()
# batsmanlistofscores.drop(['win_by_runs', 'win_by_wickets', 'delivery', 'wides', 'legbyes', 'noballs', 'byes', 'penalty',
#                           'non_boundary', 'extra_runs', 'total_runs', 'wicket'], axis=1, inplace=True)
#
# st.header('A brief Visual Journey into the Cricketing World of **IPL**')
#
#
# st.write('More often than not, it is the batsmen who get the foremost attention in T20 cricket, but, '
#          'here we shall start off with a few bowling stats. ')
#
# st.header(' **Kinds of dismissals:**')
#
# exploder = [0.1, 0, 0, 0, 0, 0]
# fig, ax = plt.subplots()
# plt.pie(deliveries['kind_of_dismissal'].value_counts()[:-3], labels=deliveries['kind_of_dismissal'].value_counts()[:-3]
#         .index, startangle=232, shadow=True, autopct='%1.1f%%', explode=exploder, labeldistance=1.05)
# plt.tight_layout()
# st.pyplot(fig)
#
# st.write(" 'Catches win Matches' and catches definitely send a lot of batsmen back to the pavilion."
#          " Getting a batsman out caught is by a big margin the most common kind of dismissal.")
#
# st.header('** Distribution of the total number of wickets falling in an inning **')
#
# fig = sns.catplot(data=matchscores, x='wicket', kind='count', aspect=2)
# fig.set_axis_labels(x_var="Total # of wickets")
# st.pyplot(fig)
# st.write("An innings ending with just 1, 2 or No wickets falling is quite rare.")
# st.write('')
#
# st.subheader('Does the above distribution hold true for both the first and second innings individually?')
#
# fig = sns.catplot(data=matchscores, x='wicket', kind='count', col='innings')
# axes = fig.axes.flatten()
# axes[0].set_xlabel("# of Wickets")
# axes[1].set_xlabel("# of Wickets")
#
# st.pyplot(fig)
# st.write("Regarding 1st innings, we may claim that it is likely that a total of 4 to 8 wickets would fall."
#          " Regarding 2nd innings, while teams are chasing, a total of just 0 or 1 wicket falling is rare while "
#          "the distribution is fairly uniform for the remaining counts of total wickets.")
#
# st.write("These graphs also show that chasing teams get all-out more often than the teams setting the target."
#          " Could it be the nerves getting to them while chasing targets?")
#
#
# st.header("Distribution of the number of wickets falling in an inning (Team-wise)")
# st.write("For the sake of keeping the comparison concise, let us consider only Four teams.")
# grid = sns.catplot(data=matchscores[(matchscores["batting_team"] == 'MI') | (matchscores["batting_team"] == 'RCB') |
#                                     (matchscores["batting_team"] == "SRH") | (matchscores["batting_team"] == "CSK")],
#                    x='wicket', kind='count', col='batting_team', col_wrap=2)
# for ax in grid.axes:
#     ax.tick_params(labelleft=True, labelbottom=True)
#     ax.set( xlabel='# of Wickets')
# plt.tight_layout()
# st.pyplot(grid)
# st.write("These graphs may explain why CSK and MI are so successful."
#          " They just don't lose too many wickets that often. Their batsmen usually finish the job and don't leave it"
#          " for the tail-enders. ")
#
# st.subheader("Moving on now to some stats regarding runs scored,")
# st.header("Distribution of runs scored in an inning")
#
# fig = sns.displot(data=matchscores, x='total_runs', kind='hist', bins=25, aspect=2)
# st.pyplot(fig)
# st.write(" The histogram of Inning totals is centred around about 160 with the bulk of the totals between 130 to 170.")
#
# st.header("How many runs do teams usually win by: ")
# fig = sns.displot(data=matches, x='win_by_runs', kind='hist', bins=18, aspect=2)
# st.pyplot(fig)
# st.write(" Teams chasing often falter within 20 runs from the target score.")
#
# st.header("Over-wise stats:")
# st.write("In the following visualizations we shall see how things unravel when the data is seen over-wise.")
#
# st.header("Over-wise average Run Rate")
#
# overs = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh',
#          'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth',
#          'twentieth']
# fig = sns.catplot(data=deliveries.groupby(['match_id', 'innings', 'over']).agg(np.sum).reset_index().groupby('over')
#                 .agg(np.mean).reset_index(), x='over', y='total_runs', aspect=2, kind='bar', order=overs)
# fig.set_xticklabels(rotation=30, horizontalalignment='right')
# fig.set(ylabel='Average Run Rate', xlabel='Over')
# st.pyplot(fig)
# st.write("As expected, the flow of runs slows down after the end of PowerPlay overs and then again picks up steadily"
#          " until the end of the innings with the overs 16 through 20 seeing the highest average Run Rates.")
#
# st.header("Over-wise falling of Wickets")
#
# fig3 = sns.catplot(data=deliveries.groupby('over').agg(np.sum).reset_index(), kind='bar', x='over', y='wicket',
#                    aspect=2, order=overs)
# fig3.set_xticklabels(rotation=30, horizontalalignment='right')
# fig3.set(ylabel='Total # of Wickets', xlabel='Over')
# st.pyplot(fig3)
#
# st.write(" Just like average Run Rate, the fall of wickets too takes a slight halt right after the end of powerplay overs"
#          " and then rises steadily as the innings draws to a close with the death overs having seen the fall of"
#          " lots of wickets.")
#
# st.write(" If you are one of those people who are into fantasy cricket team building, this graph may tell you that"
#          " bowlers who bowl at the beginning and then at the death overs have the most chances of bringing you"
#          " points by getting wickets.")
#
# st.write("Correlation surely does not always imply causation, but looking at the above two graphs of Overwise Average Runs"
#          " scored and Overwise-Wickets fallen we can claim that Higher Run Rates has been causing higher number of Wickets"
#          " to fall."
#          " Batsmen looking to score faster by taking extra risk create extra chances of wicket falling.")
#
# st.header("The relation between a Player's age and his contributions")
#
# ages = match_points.groupby('matchday_player_age').agg(np.sum).reset_index()
# ages['matchday_player_age'] = ages['matchday_player_age'].astype(int)
# sns.set_context("notebook")
# fig = sns.catplot(data=ages, x='matchday_player_age',
#                   y='total_points', kind='bar', aspect=2)
# fig.set_xticklabels(rotation=30, horizontalalignment='right')
# st.pyplot(fig)
# st.write(" What a beautiful near Normal Distribution! IPL has seen peak performance and most contribution from"
#          " players when aged around 26-27 years.")
#
# st.write("The above visualization took a little extra bit of effort on account of having to hunt for player DOBs"
#          " and matching the names of players in the newly scraped data with the names of players in the existing data being"
#          " used from another source.")
#
# st.write(" **Note:** The data used in above visualization includes player contribution in all aspects i.e. points have"
#          " been assigned to Runs scored, Wickets taken and other contributions on the Field as per Fantasy Cricket norms.")
#
#
# st.header(" The Importance and Impact of Boundaries")
# st.write(" Boundaries seem to be the cynosure of all eyes in the T20 format."
#          " Big Hits and Big Hitters are clear crowd favourites."
#          " More than 55% of all runs scored in the tournament have come via boundaries."
#          " Boundaries move the scoreboard at a faster pace and put real extra pressure on the bowler"
#          " and on the bowling team causing an upset in their strategies.")
#
# deliveries_boundaries = deliveries[(deliveries['non_boundary'] == 0) & ((deliveries['batsman_runs'] == 4) |
#                                                                         (deliveries['batsman_runs'] == 6))]
#
# # preparing batsman wise data OR overwise data for analysis with boundaries
# deliveries_boundaries.drop(['delivery', 'non_striker', 'wides', 'legbyes', 'noballs', 'byes', 'penalty', 'non_boundary',
#                             'extra_runs', 'total_runs', 'wicket', 'player_out', 'kind_of_dismissal', 'fielders'],
#                            axis=1, inplace=True)
# deliveries_boundaries['fours'] = np.where(deliveries_boundaries['batsman_runs'] == 4, 1, 0)
# deliveries_boundaries['sixes'] = np.where(deliveries_boundaries['batsman_runs'] == 6, 1, 0)
# # Let us see how boundaries are scored overwise
# over_boundaries = deliveries_boundaries.groupby('over').agg(np.sum).reset_index().drop(['match_id'], axis=1)
#
# st.header("Number of Fours hit, Over-wise")
# sns.set_context("talk")
# fig = sns.catplot(data=over_boundaries, kind='bar', x='over', y='fours', order=overs, aspect=2)
# fig.set_xticklabels(rotation=30, horizontalalignment='right')
# st.pyplot(fig)
# st.write("Powerplay overs are where most of the Fours of the innings have been hit.")
#
# st.header("Number of Sixes hit, Over-wise")
# fig = sns.catplot(data=over_boundaries, kind='bar', x='over', y='sixes', order=overs, aspect=2)
# fig.set_xticklabels(rotation=30, horizontalalignment='right')
# st.pyplot(fig)
#
# st.write("Sure, the batsmen send a few out of the park in Powerplay overs but the real flurry of Sixes takes place during "
#          "the death overs of the innings where batsmen want to give a big push to the team total."
#          " This is also due to the fact that batsmen wouldn't mind risk losing their wicket by taking the aerial "
#          "route since the innings is coming to a close anyway. This may explain why we see more Sixes than Fours "
#          "during death overs.")
#
# st.header("It is now time to **Finish it off in Style ** ;)")
#
# st.write("The following graph plots the total number of runs scored by MS Dhoni in *just* boundaries alone in each over.")
# # Dhoni and his boundaries
# over_boundaries = deliveries_boundaries.groupby(['match_id', 'innings', 'batting_team', 'bowling_team', 'over', 'striker', 'bowler']).agg(np.sum).reset_index()
# MSD = over_boundaries[over_boundaries['striker'] == 'MS Dhoni'].groupby('over').agg(np.sum).reset_index()
#
# fig = sns.catplot(data=MSD, kind='bar', x='over', y='batsman_runs', order=overs, aspect=1.75, color='yellow')
# fig.set_xticklabels(rotation=30, horizontalalignment='right')
# fig.set(ylabel='Total Runs scored by MSD in Boundaries', xlabel='Over')
# st.pyplot(fig)
#
# st.write("This graph shows why MSD is considered to be one of the most dangerous Finishers."
#          "The increase in the number of runs he scores in boundaries towards the end of the innings is *almost*"
#          " exponential!"
#          " As an opponent you just do not want MSD at the crease during the final overs.")
#
# st.write("** ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ **")
