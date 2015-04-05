import sys
import requests
from bs4 import BeautifulSoup

MIN_RECORD = 987 ; MAX_RECORD = 10000

class DocumentManager():
    """
    Downloads xml and pdf for articles in the SCOAP3 repository.
    """
    def __init__(self, xml_output, pdf_output):
        self.xml_output = xml_output
        self.pdf_output = pdf_output

    def get_publisher(self, html):
        """
        Retrieves publisher meta data field--if present--from html document.
        """
        soup = BeautifulSoup(html)
        try:
            return soup.find("meta", {"name":"citation_publisher"})['content']
        except TypeError:
            return None

    def retrieve_training_documents(self, publisher):
        """
        Downloads xml and pdf for articles in the SCOAP3 repository.
        """
        pdfs_downloaded = 0 ; xmls_downloaded = 0

        for i in xrange(MIN_RECORD, MAX_RECORD):
            try:
                page = 'http://repo.scoap3.org/record/%s' % (i)
                html = requests.get(page)
                if self.get_publisher(html.content) != publisher:
                    continue
                xml = requests.get(page + '/files/fulltext.xml')
                pdf = requests.get(page + '/files/fulltext.pdf?subformat=pdfa')

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
            except requests.exceptions.SSLError:
                print 'Invalid certificate'
                continue
            except IOError:
                print 'Output folder not found'
                continue
            except KeyboardInterrupt:
                sys.exit()
            except:
                print 'Could not retrieve document'
                continue

        print "\nStats:"
        for str, val in (('XMLs downloaded', xmls_downloaded),
                         ('PDFs downloaded', pdfs_downloaded)):
            print '\t%s: %d' % (str, val)

if __name__ == '__main__':
    dm = DocumentManager('scoap_xmls/', 'scoap_pdfs/')
    dm.retrieve_training_documents('Hindawi Publishing Corporation')