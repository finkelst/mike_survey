#!/usr/bin/env python

import cgi
import json
#blf changed to relative file path 3/15
f = open('../users.txt', 'r')
last_user = int(f.read())
f.close()

form = cgi.FieldStorage()

data = {}

if 'id_number' in form:
	# f = open('users2.txt', 'w')
	# f.write(form['id_number'].value)
	# f.close()

	#check if id is valid
	data['valid_user'] = (int(form['id_number'].value) <= last_user)

else:
	data['id_number'] = last_user + 1
	#update file
	#blf changed to relative file path 3/15
	f = open('../users.txt', 'w')
	f.write(str(last_user + 1))
	f.close()

print "Content-type: application/json"
print
print json.dumps(data)
