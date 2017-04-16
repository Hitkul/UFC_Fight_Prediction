import requests
from bs4 import BeautifulSoup
import json
import urllib2

record = {}
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
	# print str(event_id)
	# http://m.ufc.com/fm/api/event/detail/816.json
	url = "http://m.ufc.com/fm/api/event/detail/"+str(event_id)+".json"
	# print url
	data = json.load(urllib2.urlopen(url))
	# print data
	json_for_each_fight = data["FightCard"]
	for fight in json_for_each_fight:
		fight_id = fight["statid"]
		json_for_each_fighter = fight["Fighters"]
		for fighter in json_for_each_fighter:
			if fighter["Outcome"]["OutcomeID"] == "1"  :
				winning_fighter_id = fighter["statid"]
				record[str(event_id)+"_"+str(fight_id)] = winning_fighter_id
				break;
			elif fighter["Outcome"]["OutcomeID"] == "4":
				record[str(event_id)+"_"+str(fight_id)] = "00000"# no contest
				break;
			elif fighter["Outcome"]["OutcomeID"] == "3":
				record[str(event_id)+"_"+str(fight_id)] = "11111"#draw
				break;
	# print h
	# with open('json/'+str(event_id)+"_"+str(h)+'.json', 'w') as outfile:
 #    		json.dump(data, outfile)	


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
# print record
with open('winners.json', 'w') as outfile:
     		json.dump(record, outfile, indent=4)
