import pandas as pd
import os
import numpy as np
import requests
from bs4 import BeautifulSoup

# this is the webpage which has a table of player overview stats, we will scrape the player IDs
# along with this table so that we can scrape further player details from other web pages on this website
# using these player IDs

url = 'http://www.howstat.com/cricket/Statistics/IPL/PlayerList.asp?s=XXXX'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

headings = ['Name', 'Teams', 'Matches', 'Runs', 'Bat avg', 'Wickets', 'Bowl avg']
playerids = []

# Scraping PlayerIDs from this web page
data = []
playerstable = soup.find('table', class_='TableLined')
rows = playerstable.find_all('tr')
for row in rows:
    t_rows = {}
    for col, heading in zip(row.find_all('td'), headings):
        t_rows[heading] = col  # .text.strip()
    data.append(t_rows)

dataDF = pd.DataFrame(data)
for i in dataDF.Name:
    pid = str(i.a).split('PlayerID=')
    id_1 = pid[-1].split('">')
    player_id = id_1[0]
    playerids.append(player_id)

# scraping the table as is
data = []
playerstable = soup.find('table', class_='TableLined')
rows = playerstable.find_all('tr')
for row in rows:
    t_rows = {}
    for col, heading in zip(row.find_all('td'), headings):
        t_rows[heading] = col.text.strip()
    data.append(t_rows)

dataDF = pd.DataFrame(data)

dataDF = dataDF.iloc[1:]
del playerids[0]

dataDF['PlayerID'] = playerids
dataDF['Runs'] = dataDF['Runs'].apply(pd.to_numeric, errors='coerce')

# To scrape D.O.B of all players in this dataframe using the scraped player IDs

DOB = []
baseurl = 'http://www.howstat.com/cricket/Statistics/IPL/PlayerOverview.asp?PlayerID='
for i in dataDF['PlayerID']:
    playerurl = baseurl + i
    playerpage = requests.get(playerurl)
    soup = BeautifulSoup(playerpage.content, 'html.parser')
    tables = soup.find_all('table')
    tableofbirth = tables[5]
    rows = tableofbirth.find_all('tr')
    row = rows[5]
    tempday = []
    for col in row.find_all('td'):
        tempday.append(col.text.strip())
    DOB.append(tempday[1])

dataDF['DOB'] = DOB
dataDF['DOB'] = pd.to_datetime(dataDF['DOB'])
today = pd.to_datetime('today')
dataDF['Age'] = (today - dataDF['DOB']).astype('<m8[Y]')

dataDF[['Matches', 'Bat avg', 'Wickets', 'Bowl avg', 'PlayerID']] = \
    dataDF[['Matches', 'Bat avg', 'Wickets', 'Bowl avg', 'PlayerID']].apply(pd.to_numeric, errors='coerce')

dataDF = dataDF.sort_values('Runs', ascending=False)
dataDF.reset_index(drop=True, inplace=True)

# Changing the names in the above DataFrame to help merge this data with the Data obtained from cricsheet.org
newname = []

for i in dataDF['Name']:
    i = i.split(',')

    if len(i) > 1:
        i[-1] = i[-1].replace(' ', '')  # removing spaces between inititals

    i = i[::-1]
    i = ','.join(i)
    i = i.replace(',', ' ')
    newname.append(i)

os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')
matchteam = pd.read_csv('IPL_matchwise_player_points.csv')
matchteam = matchteam.groupby('player').agg(np.sum)
matchteam.sort_values('player_runs', ascending=False, inplace=True)
matchteam.reset_index(drop=False, inplace=True)

# now lets compare newnames and player from matchteam
for i, j, k in zip(range(len(newname)), newname, matchteam['player']):
    if j != k:  # all those that are not same name strings
        print(i, j, k)
# we could automate the correction of almost 500+ names, we take that as a major win.
# But we still have to manually correct the remaining names

# manually correcting names
newname[35] = 'JP Duminy'
newname[52] = 'DJ Bravo'
newname[141] = 'LA Pomersbach'
newname[149] = 'B Chipli'
newname[150] = 'A Ashish Reddy'
newname[152] = 'SO Hetmyer'
newname[224] = 'Niraj Patel'
newname[229] = 'KK Cooper'
newname[241] = 'MS Gony'
newname[296] = 'KB Arun Karthik'
newname[317] = 'DJ Thornely'
newname[329] = 'B Sumanth'
newname[344] = 'P Simran Singh'
newname[356] = 'A Choudhary'
newname[360] = 'MA Khote'
newname[373] = 'Harpreet Brar'
newname[420] = 'T Kohli'
newname[426] = 'X Thalaivan Sargunam'
newname[441] = 'TM Srivastava'
newname[473] = 'VRV Singh'
newname[475] = 'A Dananjaya'
newname[494] = 'S Randiv'
newname[519] = 'Anand Rajan'
newname[522] = 'S Sandeep Warrier'
newname[528] = 'Harmeet Singh (2)'
newname[529] = 'Tejas Baroka'
newname[532] = 'TP Sudhindra'
newname[542] = 'SS Agarwal'
newname[546] = 'RA Shaikh'
newname[558] = 'O Thomas'
newname[562] = 'Y Prithvi Raj'
newname[572] = 'P Suyal'


# missing in matchteam built from dataframe deliveries are :

# 523 D Joseph
# 527 R Pawar
# 566 T Mishra
# 567 KH Devdhar
# 575 P Dharmani

# checking if Name column and newname list all match
# correctly before we proceed with replacing column with newname
for i, j in zip(dataDF['Name'], newname):
    print(f"{i} ====== {j}")

# they're all right. Go ahead with replace column
newname = pd.Series(newname)
dataDF['newname'] = newname
dataDF.drop('Name', axis=1, inplace=True)
dataDF.rename(columns={'newname': 'Name'}, inplace=True)
dataDF = dataDF[['Name',  'Age', 'Teams', 'Matches', 'Runs', 'Bat avg', 'Wickets', 'Bowl avg',
                 'DOB', 'PlayerID']]
# Web scraping to Add a column for nationality of the player
base_url_1 = 'http://www.howstat.com/cricket/Statistics/Players/PlayerOverviewSummary.asp?PlayerID='
Nations = []
for i in dataDF['PlayerID']:
    nationurl = base_url_1 + str(i)
    nationpage = requests.get(nationurl)
    soup = BeautifulSoup(nationpage.content, 'html.parser')
    tables_n = soup.find_all('table')
    tableofnation = tables_n[2]
    Nations.append(tableofnation.text.strip().split('(')[-1].replace(')', ''))

dataDF['Nationality'] = Nations


# Manually setting nationality for uncapped players as they do not have nationality mentioned on the website

nations_1 = []

for i, j in zip(dataDF['Nationality'], dataDF['PlayerID']):
    if i != '':
        nations_1.append(i)

    if i == '':
        if j in [4073, 4400, 4544, 4052, 4679, 4055, 4086, 4404, 4080, 4051, 4948, 4408, 4146, 4097, 4112, 4379, 4054,
                 4072,
                 4056, 4030, 4094, 4036, 4157, 4107, 4049, 4943, 4186, 4139, 4179, 4931, 4154, 4166, 4041, 4668, 4103,
                 4032, 4378, 4113, 4163, 4756, 4047, 4098, 4136, 5866, 4125, 4180, 4029, 4114, 4147, 5863, 4042, 4132,
                 4111, 4543, 4079, 4057, 4106, 4541, 4665, 4131, 4196, 4159, 4134, 4140, 4085, 4401, 4121, 4076, 4142,
                 4194, 4153, 4050, 4102, 5857, 4197, 4122, 4183, 4155, 4059, 4192, 962, 4190, 4751, 4141, 4659, 4392,
                 4937,
                 4128, 4129, 4130, 4216, 4043, 4058, 4074, 4144, 4394, 4768, 4170, 4766, 5849, 4077, 4935, 4133, 4678,
                 4152, 4100, 4206, 4949, 4405, 4118, 4045, 4145, 4193, 4398, 4167, 4755, 4303, 4655, 4087, 4549, 4092,
                 4151, 4938, 4116, 4081, 4135, 4556, 4156, 4779, 4161, 5019, 4075, 4409, 5851, 4559, 4096, 4203, 4040,
                 4177, 4942, 4377, 4184, 4673, 4091, 5856, 4181, 4930, 4200, 4149, 4150, 4026, 4101, 4088, 4119, 4148,
                 4176, 4165, 4160, 5861, 4124, 4411, 4172, 4933, 4105, 4188, 4749, 4126, 4385, 4162, 4168, 4175,
                 4095, 4663, 4775, 4210, 4082, 4669, 4174, 4205, 4138, 4658, 4191, 4204, 4208, 4178, 4211, 4780, 4109,
                 4545, 4110, 4939, 4555, 4207, 4173, 4753, 4189, 4071, 4213, 4195, 4053, 4158]:
            nations_1.append('India')

        elif j in [4061, 4209, 4169, 5860, 4143, 4199, 5853]:
            nations_1.append('Australia')

        elif j in [4198, 4171]:
            nations_1.append('South Africa')

        elif j in [4093, 4767]:
            nations_1.append('West Indies')

        elif j in [872]:
            nations_1.append('Sri Lanka')

        elif j in [4164]:
            nations_1.append('England')

nations_1 = pd.Series(nations_1)
dataDF['Country'] = nations_1
dataDF.drop('Nationality', axis=1, inplace=True)

os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')
dataDF.to_csv('IPL_PLayers.csv', index=False)
