from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd

s = Service(executable_path='/usr/local/bin/chromedriver')
#
driver = webdriver.Chrome(service=s)
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.maximize_window()
driver.get('https://www.amazon.in/')
driver.implicitly_wait(10)

#


# Beautiful Soup not working for sportsbookreview page
# import urllib.request
# from bs4 import BeautifulSoup as bs
# import re
# import pandas as pd

#load html content from url
# page = urllib.request.urlopen("https://docs.python.org/3/library/random.html")

# page = urllib.request.urlopen("https://www.sportsbookreview.com/betting-odds/nfl-football/money-line/")
# soup = bs(page)
#
# print(soup)