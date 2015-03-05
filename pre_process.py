"""Extract text from PDF file using PDFMiner with whitespace intact."""
"""http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library/8325135#8325135"""
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from cStringIO import StringIO

import ntpath
import os
import sys

def get_text(path):
    """From http://stackoverflow.com/a/8325135/39040."""
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def main():
	try:
		user_input = sys.argv[1]
		file_name = os.path.splitext(ntpath.basename(user_input))[0]
		print file_name

		with open((os.path.dirname(__file__) + 'input-text/%s.txt')%(file_name),'w') as f:
			f.write(get_text(user_input))
	except IndexError:
		print 'Please provide a file path!'
	except IOError:
		print 'Input/output file/folder not found!'

if __name__ == "__main__":
    main()
