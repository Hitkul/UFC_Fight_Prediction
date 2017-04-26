import re


file = open('name.txt','w') 
with open('name_ufc.txt') as openfileobject:
    for line in openfileobject:
       		if line!='\n':
       			print line
       		# hh = re.split(',| |\n',line)
       		# hh = filter(None, hh)
       			file.write(line)
       		
file.close() 