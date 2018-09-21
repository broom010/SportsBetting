import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

print(os.getcwd())

def get_page(soup):
    nav = soup.find_all('span', class_='linkNavigation floatRight')
    try:
        return re.search('>(.*)<', str(nav[0].find_all('a')[-2])).group(1)
    except:
        return 1

stat_cat = ['RUSHING', 'RECIEVING', 'PASSING']


rush_url = ["http://www.nfl.com/stats/categorystats?tabSeq=0&season=2018&seasonType=REG&Submit=Go&experience=&archive=false&d-447263-p=", "&statisticCategory=RUSHING&conference=null&qualified=false"]
rec_url = ["http://www.nfl.com/stats/categorystats?tabSeq=0&season=2018&seasonType=REG&experience=&Submit=Go&archive=false&conference=null&statisticCategory=RECEIVING&d-447263-p=","&qualified=false"]
pass_url = "http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticCategory=PASSING&season=2018&seasonType=REG&experience=&tabSeq=0&qualified=false&Submit=Go"
URLs = [rush_url, rec_url, pass_url]



rush_cols = ['Rank', 'Player', 'Team', 'Pos', 'Att', 'Att/G', 'Yds', 'Avg', 'Yds/G', 'TDs', 'Long', '1st', '1st%', '20+', '40+', 'Fumbles']
rec_cols = ['Rank', 'Player', 'Team', 'Pos', 'Rec', 'Yds', 'Avg', 'Yds/G', 'Long', 'TDs', '20+', '40+', '1st', '1st%', 'Fumbles']
pass_cols = ['Rank', 'Player', 'Team', 'Pos','Comp', 'Att', 'Pct', 'Att/G', 'Yds', 'Avg', 'Yds/G', 'TDs', 'INTs', '1st', '1st%', 'Long', '20+', '40+', 'Sacks', 'Rate']
COLs = [rush_cols, rec_cols, pass_cols]

for k in range(0,3):
    if k == 2:
        info = []

        for i in range(1,3):

            r = requests.get(pass_url)

            soup = BeautifulSoup(r.content)

            data = soup.findAll('table', {'class' : 'data-table1'})[0]

            data_rows = data.findAll('tr') 

            for row in data_rows[1:]:
                cols = row.findAll('td')
                c = []
                for col in cols:
                    c.append(" ".join(col.text.split()))
                info.append(c)

        df = pd.DataFrame(info, columns=pass_cols)

        print(data_rows[1].findAll('td')[1].text)

        print(df.head())

        df.to_csv('NFL_PASSING.csv', index=False)


    else: 
        info = []

        for i in range(1,get_page(BeautifulSoup(requests.get(URLs[k][0] + str(1) + URLs[k][1]).content))+1):

            r = requests.get(URLs[k][0] + str(i) + URLs[k][1])

            soup = BeautifulSoup(r.content)

            data = soup.findAll('table', {'class' : 'data-table1'})[0]

            data_rows = data.findAll('tr') 

            for row in data_rows[1:]:
                cols = row.findAll('td')
                c = []
                for col in cols:
                    c.append(" ".join(col.text.split()))
                info.append(c)

        df = pd.DataFrame(info, columns=COLs[k])

        print(data_rows[1].findAll('td')[1].text)

        print(df.head())

        df.to_csv('NFL_' + stat_cat[k] + '.csv', index=False)






