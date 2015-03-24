import json
import requests

f = open('training/records-core-10k.json')
training_data = json.load(f)
f.close()

for doc in training_data:
	try:
		r = requests.get('inspire.net/' + doc['id'])
	except:
		print 'Could not retrieve ' + doc['id']
		continue
