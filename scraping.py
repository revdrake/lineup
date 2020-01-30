from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

bets = pd.DataFrame(columns=['site','sport','team_1','team_2','team_1_bet','team_2_bet'])
site_tags = {'Bovada':{'Name': ['name'], 'Lines':['bet-price','empty-bet']},
              'BetOnline':{'Name':['col_teamname bdevtt'],'Lines':['odds bdevtt moneylineodds displayOdds']}
             }

url_info = {'Site': ['BetOnline',
                     'BetOnline',
                     'Bovada',
                     'Bovada',
                     'Bovada',
                    ],
            'Sport': ['NFL',
                      'NHL/VHL',
                      'NBA',
                      'NFL',
                      'NHL/VHL',
                     ],
            'URL':['https://www.betonline.ag/sportsbook/football/nfl',
                   'https://www.betonline.ag/sportsbook/hockey/nhl',
                   'https://www.bovada.lv/sports/basketball/nba',
                   'https://www.bovada.lv/sports/football',
                   'https://www.bovada.lv/sports/hockey',
                  ],}

sites, sports, urls = url_info['Site'], url_info['Sport'], url_info['URL']

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/drake.hilliard/Desktop/chromedriver", options=options)

for site, sport, url in zip(sites, sports, urls):
    driver.get(url)
    time.sleep(3) # need, not only on clicks
    page_source = driver.page_source

    soup = BeautifulSoup(page_source)
    team_names = [tag.text for tag in soup.find_all(class_=site_tags[site]['Name'])]

    if site == 'BetOnline':
        money_lines = [tag.text for tag in soup.find_all(class_=site_tags[site]['Lines'])]
    elif site == 'Bovada':
        bet_prices = [tag.text for tag in soup.find_all(class_=site_tags[site]['Lines'])]
        money_lines = [bp for i, bp in zip(range(len(bet_prices)),bet_prices) if (i+1) % 6 in (3,4)]

    teams_bets = [(i,t,b) for i,t,b in zip(range(len(team_names)),team_names, money_lines)]

    team_1 = [tb[1] for tb in teams_bets if tb[0]%2 == 0]
    team_2 = [tb[1] for tb in teams_bets if tb[0]%2 != 0]
    team_1_bet = [tb[2] for tb in teams_bets if tb[0]%2 == 0]
    team_2_bet = [tb[2] for tb in teams_bets if tb[0]%2 != 0]

    bets_df = pd.DataFrame({'site': site,
                            'sport':sport,
                            'team_1': team_1,
                            'team_2': team_2,
                            'team_1_bet': team_1_bet,
                            'team_2_bet': team_2_bet,})

    bets = bets.append(bets_df, ignore_index=True)

for b in bets.columns:
    bets[b] = bets[b].str.strip()

for col in ['team_1_bet', 'team_2_bet']:
    bets.loc[bets[col]=='EVEN',col] = '100'

def is_int(someshit,r=True):
    try:
        int(someshit)
    except:
        r = False

    return r

def sign(x):
    if is_int(x):
        if int(x) > 0:
            r = 1
        elif int(x) < 0:
            r = -1
        else:
            r = 0
    else:
        r = ''

    return r

def moneyline_factor(k):
    (int(k) / 100) ** sign(int(k))

bets
bets_bovada = bets[bets['site']=='Bovada']
bets_betonline = bets[bets['site']=='BetOnline']
bets_joined = bets_bovada.merge(bets_betonline, how='inner', on=['sport','team_1','team_2'])
