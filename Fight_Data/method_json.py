import requests
from bs4 import BeautifulSoup
import json
import urllib2

methods = {}
event_id = 0
winners = {}
master_dict = {}

with open('winners.json') as data_file:    
    winners = json.load(data_file)
links = []

def spider(max_pages):
	start_year =2014
	while start_year <= max_pages:
		url = 'http://www.ufc.com/event/Past_Events?year='+str(start_year)
		source_code = requests.get(url, allow_redirects=False)
		plain_text = source_code.text.encode('ascii', 'replace')
		soup = BeautifulSoup(plain_text,'html.parser')
		for link in soup.findAll('td',{'class': 'event-title'}):
			# print link
			for href in link.findAll('a'):
				# print href
				foo = href.get('href')
				links.append(foo)
			# print(title)
		start_year+=1;

def get_json():
	url = "http://liveapi.fightmetric.com/V1/"+str(event_id)+"/Fnt.json"
	data = json.load(urllib2.urlopen(url))
	json_for_each_fight = data["FMLiveFeed"]["Fights"]
	for fight in json_for_each_fight:
		method = fight["Method"]
		fight_id = fight["FightID"]
		methods[str(event_id)+"_"+fight_id] = method

def get_ids(link):
		url = 'http://www.ufc.com'+link
		source_code = requests.get(url, allow_redirects=False)
		plain_text = source_code.text.encode('ascii', 'replace')
		source = plain_text
		edit  = source[source.find("document.refreshURL =")+57:source.find("document.refreshURL =")+60]
		global event_id
		event_id = edit
		print event_id
		get_json()


spider(2017)
for link in links:
	get_ids(link)

# print winners

for fight in winners:
	master_dict[fight] = [winners[fight],methods[fight]]
print master_dict
with open('result.json', 'w') as outfile:
     		json.dump(master_dict, outfile, indent=4)
