import json
import requests
import re
import sys

MIN_RECORD = 1000 ; MAX_RECORD = 10000

class DocumentManager():
    """
    Downloads xml and pdf for articles in the SCOAP3 repository.
    """
    def __init__(self, xml_output, pdf_output):
        self.xml_output = xml_output
        self.pdf_output = pdf_output

    def retrieve_training_documents(self):
        """
        Downloads xml and pdf for articles in the SCOAP3 repository.
        """
        pdfs_downloaded = 0 ; xmls_downloaded = 0

        for i in xrange(MIN_RECORD, MAX_RECORD):
            try:
                page = 'http://repo.scoap3.org/record/%s' % (i)
                xml = requests.get(page + '/files/main.xml')
                pdf = requests.get(page + '/files/main.pdf?subformat=pdfa')

                if xml.status_code != 404:
                    f = open(self.xml_output + '%s.xml' % (i), "wb")
                    f.write(xml.content)
                    f.close()
                    xmls_downloaded += 1

                if pdf.status_code != 404:
                    f = open(self.pdf_output + '%s.pdf' % (i), "wb")
                    f.write(pdf.content)
                    f.close()
                    pdfs_downloaded += 1
                print '\rCompleted: %.02f%%' %\
                    (100. * (i + 1 - MIN_RECORD) / (MAX_RECORD - MIN_RECORD)),
                sys.stdout.flush()
            except IOError:
                print 'Output folder not found...'
                continue
            except:
                print 'Could not retrieve document...'
                continue

        print "\nStats:"
        for str, val in (('XMLs downloaded', xmls_downloaded),
                         ('PDFs downloaded', pdfs_downloaded)):
            print '\t%s: %d' % (str, val)

if __name__ == "__main__":
    dm = DocumentManager("scoap_xmls/", "scoap_pdfs/")
    dm.retrieve_training_documents()