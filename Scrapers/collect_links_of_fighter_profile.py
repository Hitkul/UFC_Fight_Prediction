
import requests
from bs4 import BeautifulSoup

def collect_links(max_pages):
	offset =0 
	links = list()
	while offset <= max_pages:
		print(offset,max_pages)
		url = 'http://www.ufc.com/fighter/Weight_Class?offset='+str(offset)+'&max=20&sort=lastName&order=asc&weightClass=null&fighterFilter=All'
		source_code = requests.get(url, allow_redirects=False)
		plain_text = source_code.text.encode('ascii', 'replace')
		soup = BeautifulSoup(plain_text,'html.parser')
		for link in soup.findAll('a',{'class': 'fighter-name'}):
			links.append(link.get('href'))
		offset += 20
	return links


links = collect_links(2185)
batch_size = 100
list_of_links = [links[x:x+batch_size] for x in range(0,len(links),batch_size)]

for i,links in enumerate(list_of_links):
	with open(f'data/profile_links/fighter_profile_links{i}.txt', 'w') as fp:
		for link in links:
			fp.write(link+'\n')
