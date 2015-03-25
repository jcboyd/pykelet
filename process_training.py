import json
import requests
import re

MAX_DOWNLOAD = 1000

class DocumentManager():
	def __init__(self, records, output):
		self.records = records
		self.dir = output

	def load_records(self):
		f = open('training/records-core-10k.json')
		self.records = json.load(f)
		f.close()

	def retrieve_training_documents(self):
		num_downloaded = 0

		for article in self.records:
			try:
				for doc in article['filenames']:
					if re.match(r'arXiv(.*)\.pdf', doc):
						doc = doc.replace(':', '.org/pdf/').replace('_', '/')
						print 'Downloading %s...'%(doc)
						r = requests.get("http://" + doc)
						if r.status_code != 404:
							f = open(self.dir + doc.replace("/", "_"), "wb")
							f.write(r.content)
							f.close()
							num_downloaded += 1
				if num_downloaded == MAX_DOWNLOAD:
					break
			except KeyError:
				print 'Dictionary key not found...'
				continue
			except IOError:
				print 'Output folder not found...'
				continue
			except:
				print 'Could not retrieve document...'
				continue

if __name__ == "__main__":
	retrieve_training_documents()