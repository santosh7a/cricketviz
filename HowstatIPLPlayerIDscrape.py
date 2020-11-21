import datetime
import pandas as pd
import os
start_time = pd.to_datetime('now')
import numpy as np
import requests
from bs4 import BeautifulSoup

# this is the page which has a table of player overview stats, we will scrape the player ids
# along with this table so that we can scrape further details of these playerids

url = 'http://www.howstat.com/cricket/Statistics/IPL/PlayerList.asp?s=XXXX'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

headings = ['Name', 'Teams', 'Matches', 'Runs', 'Bat avg', 'Wickets', 'Bowl avg']
playerids = []

# Scraping PlayerIDs from this table
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
    id = str(i.a).split('PlayerID=')
    id_1 = id[-1].split('">')
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
dataDF = dataDF.sort_values('Runs', ascending=False)

# To scrape D.O.B of all players in this dataframe
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
os.chdir(r'C:\\Users\\santosh\\PycharmProjects\\Cricket')
#dataDF.to_csv('IPLPLayers.csv')