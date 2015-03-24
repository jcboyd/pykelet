import json
import requests
import re

def retrieve_training_documents():
    f1 = open('training/records-core-10k.json')
    core_records = json.load(f1)
    f1.close()

    f2 = open('training/records-curated-10k.json')
    curated_records = json.load(f2)
    f2.close()

    for doc in core_records:
	try:
    	    for file_name in doc['filenames']:
                if re.match('arXiv(.*)\.pdf', a):
		    break
	    print 'Downloading'
	    r = requests.get('arxiv.org/pdf/' + file_name)
    	    name = doc
	    with open(output + name + ".pdf", "wb") as output_file:
		output_file.write("output/" + r.content)
	except KeyError:
	    print 'File key not found...'
	    continue
	except:
	    print 'Could not retrieve ' + doc['id']
	    continue

if __name__ == "__main__":
	retrieve_training_documents()
