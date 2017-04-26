import requests
from bs4 import BeautifulSoup
import json
import urllib2

fight_id = []
event_id = 0

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
	for h in fight_id:
		print h+"    "+str(event_id)
		url = "http://liveapi.fightmetric.com/V2/"+str(event_id)+"/"+str(h)+"/Stats.json"
		# print url
		data = json.load(urllib2.urlopen(url))
		# print h
		with open('json/'+str(event_id)+"_"+str(h)+'.json', 'w') as outfile:
	    		json.dump(data, outfile)	


def get_ids(link):
		url = 'http://www.ufc.com'+link
		source_code = requests.get(url, allow_redirects=False)
		plain_text = source_code.text.encode('ascii', 'replace')
		source = plain_text
		#fight id
		edit  = source[source.find("fightOutcomeData"):]
		foo = edit.split(";")
		bar = foo[0][foo[0].find("{"):]
		bar = bar[1:-1]
		sheep = bar.split(",")
		for h in sheep:
			fight_id.append(h[:h.find(":")][1:-1])
		# print fight_id
		source = plain_text
		edit  = source[source.find("document.refreshURL =")+57:source.find("document.refreshURL =")+60]
		global event_id
		event_id = edit
		get_json()


spider(2017)
for link in links:
	fight_id=[]
	get_ids(link)



