#! python3
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/84.0.4316.21'}
    url = f'https://uk.indeed.com/jobs?q=software+development+engineer&l=United+Kingdom&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    jobs = soup.find_all('a', class_ = 'tapItem')
    for item in jobs:
        title = item.find('h2',{'class':'jobTitle'}).find('span', {"class": False}).text.strip()
        try:
            company = item.find('span',{'class':'companyName'}).find('a').text.strip()
        except:
            company=''
        try:
            salary = item.find('div', class_ = 'salary-snippet').find('span').text.strip()
        except:
            salary = ''
        location = item.find('div', {'class' : 'companyLocation'}).text.strip()
        link = item['href']

        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'location':location,
            'link':link
        }
        joblist.append(job)
    return

joblist = []  

for i in range(0,50,10):
    print(f'Getting page, {i}')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')
