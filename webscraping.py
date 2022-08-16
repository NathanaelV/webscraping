import time
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# 1. Pegar conteúdo HTML a partir da URL
url = 'https://www.nba.com/stats/players/traditional/?sort=PTS&dir=1'

option = Options()
option.headless = False # Mudar para True para não ver o navegador em ação
driver = webdriver.Firefox(options=option)

driver.get(url)
time.sleep(2)

path = "//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']"
driver.find_element_by_xpath(path).click()

element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')


# 2. Parsear o conteúdo HTML - BeaultifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


# 3. Estruturar conteúdo em Data Frame - Pandas

df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']


# 4. Transformar os Dados em um Dicionário de dados próprio

top10ranking = {}
top10ranking['points'] = df.to_dict('records')

driver.quit()


# 5. Converter e salvar em um arquivo JSON

js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close

