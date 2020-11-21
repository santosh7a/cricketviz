#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

import seaborn as sns
import matplotlib.pyplot as plt
baseurl='http://www.howstat.com/cricket/Statistics/PlayerProgressBat.asp?PlayerID='
url='http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp'
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
headings=['Name','Born','Country','Tests','ODIs','T20s']
playerids=[]
playernames=[]

data=[] 
playerstable=soup.find('table',class_='TableLined')
rows=playerstable.find_all('tr')
rows=rows[1:]
for row in rows:
    t_rows={}
    for col,heading in zip(row.find_all('td'),headings):
        t_rows[heading]=col
    data.append(t_rows)
    
dataDF=pd.DataFrame(data)

dataDF=dataDF.iloc[1:-1]

for i in dataDF['Name']:
    id=str(i.a).split('ID=')
    id_1=id[-1].split('">')
    player_id=id_1[0]
    playerids.append(player_id)
    player_name=id_1[-1].replace('</a>','')
    playernames.append(player_name)

Playersidsdf=pd.DataFrame({'ID': playerids ,'Player' : playernames })

