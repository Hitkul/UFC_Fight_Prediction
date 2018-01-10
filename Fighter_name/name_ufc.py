
import requests
from bs4 import BeautifulSoup
links = []
#scraping profile links insted of names
def trade_spider(max_pages):
	offset =0 
	while offset <= max_pages:
		print(offset,max_pages)
		url = 'http://www.ufc.com/fighter/Weight_Class?offset='+str(offset)+'&max=20&sort=lastName&order=asc&weightClass=null&fighterFilter=All'
		source_code = requests.get(url, allow_redirects=False)
		plain_text = source_code.text.encode('ascii', 'replace')
		soup = BeautifulSoup(plain_text,'html.parser')
		for link in soup.findAll('a',{'class': 'fighter-name'}):
			links.append(link.get('href'))
			# title = link.string
			# print(href)
			# print(title.encode('utf-8'))
		offset += 20


trade_spider(2064)
with open('fihter_profile_links.txt', 'w') as fp:
    for link in links:
		fp.write(link+'\n')
