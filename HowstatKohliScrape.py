# This program is how it all started, with this basic logic we scrape data of all other IPL players similarly.
import requests
from bs4 import BeautifulSoup

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Scraping data from the website
url = 'http://www.howstat.com/cricket/Statistics/IPL/PlayerProgressBat.asp?PlayerID=3600'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

headings = ['No.', 'Date', 'Versus', 'Ground', 'D/N*', 'How Dismissed ', 'Runs',
            'B/F', 'S/R', 'delete this column', 'Aggr', 'Avg', 'Aggr S/R']
data = []  # we will populate this list with dictionaries of rows
table = soup.find("table", class_='TableLined')
rows = table.find_all('tr')
rows = rows[3:]
for row in rows:
    t_row = {}
    for col, heading in zip(row.find_all('td'), headings):
        t_row[heading] = col.text.strip()
    data.append(t_row)
dataDF = pd.DataFrame(data)
dataDF.drop(['delete this column', 'D/N*'], axis=1, inplace=True)
# to be able to perform math functions on these columns we need to make it type numerical
dataDF['Runs'] = dataDF['Runs'].str.replace('*', '')
dataDF[['Runs', 'B/F', 'S/R', 'Aggr', 'Avg', 'Aggr S/R']] = \
    dataDF[['Runs', 'B/F', 'S/R', 'Aggr', 'Avg', 'Aggr S/R']].apply(pd.to_numeric, errors='coerce')

# a couple of basic visualisations
sns.scatterplot(data=dataDF, x='B/F', y='Runs', hue='S/R')
plt.show()
sns.lineplot(data=dataDF,x='No.',y='Aggr')
plt.show()
runsplot=sns.relplot(data=dataDF,x='No.',y='Runs',kind='line', aspect=3.5)
runsplot.axes[0][0].axhline(y = 30, color='black')
runsplot.axes[0][0].axhline(y = 50, color='red')
plt.show()
# those are a lot of lines above half century