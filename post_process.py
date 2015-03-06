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

    """
    ENCODING OF HEADERS - grobid/grobid-trainer/doc/GuidelinesTrainingData.pdf
    <titlePart> for title (included in a <docTitle> element).
    <docAuthor> for the complete sequence of authors.
    <affiliation> for the complete affiliation field.
    <address> for the complete address field. 
    <div type="introduction"> for the start of the introduction section (i.e. just after the header ends).
    <keyword> for the keyword field
    <email> for encoding the email address
    <phone> for encoding the contact phone number
    <ptr> for web url corresponding to the processed document (e.g. where the document is available online).
    <date type="publication"> is the publication date, which is similar to the default case
    <reference> this is to annotate the reference information about the current article present in its header.
    <idno> for the article-specific identifier, in particular DOI.
    <note type="copyright"> for the copyright info
    <note type="submission"> for the information about the submission of the document.
    <note type="dedication"> for information about the dedication of the publication.
    <note type="page"> for the page number
    <note type="english_title"> in the case that the main title is not in English.
    """

    header_data = {}
    
    header_data['idno'] = header.idno.text if header.idno is not None else None
    header_data['note'] = header.note.text if header.note is not None else None
    header_data['keywords'] = header.keywords.text if header.keywords is not None else None
    header_data['title'] = header.title.text if header.title is not None else None
    header_data['abstract'] = front.p.text if header.p is not None else None
    header_data['authors'] = [{"forename" : a.forename.text, "surname" : a.surname.text, "orgName" : a.orgname.text} \
                              for a in header.sourcedesc.biblstruct.analytic.findAll("author")]

    # Process references

    """
    ENCODING OF REFERENCES - grobid/grobid-trainer/doc/GuidelinesTrainingData.pdf
    <author> for the complete sequence of authors
    <title level="a"> for article title and chapter title.
    <title level="j"> for journal title.
    <title level="m"> for non journal bibliographical item holding the cited article.
    <date> the date sequence (including parenthesis, etc.)
    <biblScope type="pp"> the full range of pages
    <biblScope type="vol"> the block for volume (e.g. <volume> vol. 7,</volume>)
    <biblScope type="issue"> the block for the issue, also known as number.
    <orgName> the institution for thesis or technical reports
    <publisher> the name of the publisher
    <pubPlace> publication place, or location of the "publishing" institution
    <editor> for all the sequence of editors
    <ptr> for web url
    <idno> for the document-specific identifier, in particular DOI
    <note> for any indications related to the reference and not covered by one of the previous tags.
    """

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
            print "%s - %s" % (path, sm.ratio())

if __name__ == "__main__":
    main()