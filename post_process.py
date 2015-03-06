#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
import json
import difflib
import re

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

def convert_to_json(path):
    """Extract from XML output and write to JSON"""
    f = open(path, 'r')
    xml = f.read()
    f.close()

    doc = BeautifulSoup(xml)

    header = doc.tei.teiheader
    front = doc.tei.front
    back = doc.tei.back

    # Process header
    header_data = {}
    
    header_data['idno'] = header.idno.text if header.idno is not None else None
    header_data['note'] = header.note.text if header.note is not None else None
    header_data['keywords'] = header.keywords.text if header.keywords is not None else None
    header_data['title'] = header.title.text if header.title is not None else None
    header_data['abstract'] = front.p.text if header.p is not None else None
    header_data['authors'] = [{"forename" : a.forename.text, "surname" : a.surname.text, "orgName" : a.orgname.text} \
                              for a in header.sourcedesc.biblstruct.analytic.findAll("author")]       

    # Process references
    reference_data = []
    i = 0

    for reference in back.div.listbibl.findAll("biblstruct"):
        reference_data.append({})
        if reference.analytic:
            reference_data[i]["title"] = reference.analytic.title.text
            reference_data[i]["authors"] = [{"forename" : a.forename.text, "surname" : a.surname.text} \
                                            for a in reference.analytic.findAll("author")]
        if reference.monogr:
            pass
        i += 1

    return {"header" : header_data, "references" : reference_data}

def main():
    """Compare model output with ground truth"""
    json_data = open('data.json')
    json_data = json.load(json_data)
    truth = JsonDocument(json_data, '')

    meta_data = convert_to_json('output-grobid/HMM.tei.xml')
    meta = JsonDocument(meta_data['header'], '')

    for node in truth.dfs():
        value = node[0] ; path = node[1]

        if value is not None:
            sm = difflib.SequenceMatcher(None, value, meta.index(path))
            print path, "-", sm.ratio()

if __name__ == "__main__":
    main()