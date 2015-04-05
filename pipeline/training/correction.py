import os
import json
from bs4 import BeautifulSoup
import re
import sys

class JsonDocument():
    """Class for manipulating JSON document"""
    def __init__(self, document, root):
        self.document = document
        self.root = root
        
    def index(self, path):
        """Return value at path, return None if not found"""
        try:
            indices = [int(x) if x.isdigit() else x for x in re.split(r'[\/\[\]]+', path[1:])]
            return reduce(lambda x, y : x[y], indices, self.document)
        except:
            return None

    def dfs(self):
        """Depth first search on JSON hierarchy."""
        return self.__dfs(self.document, self.root)

    def __dfs(self, subtree, path):
        """Depth first search on JSON hierarchy."""
        if isinstance(subtree, list):
            for node in subtree:
                for child in self.__dfs(node, path + "[" + str(subtree.index(node)) + "]"):
                    yield child
        elif isinstance(subtree, dict):
            for node in subtree:
                for child in self.__dfs(subtree[node], path + "/" + node):
                    yield child
        else: # Leaf node
            yield (subtree, path)

def loop_over_tei():
    # Load records
    print 'Loading records...'
    records = json.load(open('training/records-core-10k.json'))
    print 'Processing files...'
    num_docs = 0 ; title_corrected = 0 ; abstract_corrected = 0
    directory = os.listdir('tei/output')
    
    for file_name in directory:
        num_docs += 1
        f = open('tei/output/' + file_name)
        doc = BeautifulSoup(f)
        f.close()

        #Get grobid extracted references
        # reference_list = doc.back.listbibl.findAll('biblstruct')

        rec_id = int(file_name.split('.')[0])
        
        ground_truth = None
        for record in records:
            if record['recid'] == rec_id:
                ground_truth = JsonDocument(record, "")

        for entry in ground_truth.dfs():
            # print entry[1]
            if entry[1].startswith('/title/title'):
                if doc.title.string != entry[0]:
                    doc.title.string = entry[0]
                    title_corrected += 1
            elif entry[1].startswith('/abstract'):
                if doc.abstract != entry[0]:
                    doc.title.string = entry[0]
                    abstract_corrected += 1

        print '\rCompleted: %.02f%%' % (num_docs * 100. / len(directory)),
        sys.stdout.flush()

    print '\nStats:'
    for str, val in (('# corrected titles', title_corrected),
                     ('# corrected abstracts', abstract_corrected),
                     ('# corrected titles', title_corrected)):
        print '\t%s: %d (%.02f%%)' % (str, val, val*100./num_docs)