from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

bets = pd.DataFrame(columns=['site','sport','team_1','team_2','team_1_bet','team_2_bet'])

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

url_info = {'Site': ['Bovada',
                     'Bovada'],
            'Sport': ['NBA',
                      'NFL'],
            'URL':['https://www.bovada.lv/sports/basketball/nba',
                   'https://www.bovada.lv/sports/football'],}

sites = url_info['Site']
sports = url_info['Sport']
urls = url_info['URL']

for site, sport, url in zip(sites, sports, urls):
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)
    driver = webdriver.Chrome("/Users/drake.hilliard/Desktop/chromedriver", options=options)
    driver.get(url)
    more_buttons = driver.find_elements_by_class_name("moreLink")
    for x in range(len(more_buttons)):
        if more_buttons[x].is_displayed():
            driver.execute_script("arguments[0].click();", more_buttons[x])
            time.sleep(4)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source)
    team_names = [tag.text for tag in soup.find_all(class_=["name"])]
    bet_prices = [tag.text for tag in soup.find_all(class_=["bet-price","empty-bet"])]

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

print(bets)
