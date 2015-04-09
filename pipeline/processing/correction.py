import json
from re import compile, split, findall
from os import environ, path, listdir
from bs4 import BeautifulSoup

class JsonDocument():

    """Class for manipulating JSON document."""

    def __init__(self, document, root):
        self.document = document
        self.root = root
        
    def index(self, path):
        """Return value at path, return None if not found."""
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

class Validator():

    """Class for validating training set produced by grobid."""
    
    def __init__(self, ground_truth_directory, bs_directory, output_directory):
        self.ground_truth_directory = ground_truth_directory
        self.bs_directory = bs_directory
        self.output_directory = output_directory

    def __reference_segmenter_correction(self, bs):
        """Rewrite reference segmentation."""
        regex = compile(r'\[[0-9]+\]')
        references = split(regex, bs.find('listBibl').text)[1:]
        labels = findall(regex, bs.find('listBibl').text)

        bs.find('listBibl').extract()
        bs.find('text').insert(0, bs.new_tag('listBibl'))

        for ref in references:
            label_tag = bs.new_tag('label')
            label_tag.string = labels[references.index(ref)]
            bibl_tag = bs.new_tag('bibl')
            bibl_tag.insert(0, label_tag)
            bibl_tag.insert(1, ref)
            bs.find('listBibl').append(bibl_tag)
    
    def reference_segmenter_validation(self):
        """Correct directory of reference_segmenter training files."""
        for file in filter(lambda x: x.endswith('referenceSegmenter.tei.xml'), listdir(self.bs_directory)):
            print "Processing", file
            bs = BeautifulSoup(open(self.bs_directory + file), 'xml')
            # find ground_truth file
            # ground_truth = BeautifulSoup(open(self.ground_truth_directory + file.split(".")[0] + '.xml'), 'xml')
            self.__reference_segmenter_correction(bs)
            file = open(output_directory + file, "wb")
            file.write(bs.prettify().encode('utf-8'))
    
    def __citation_correction(self):
        """Correct citation training TEI file."""
        pass
    
    def citation_validation(self):
        """Correct directory of citation training files."""
        for file in filter(lambda x : x.startswith('citation'), os.listdir(bs_directory)):
            print "Processing", file
            bs = BeautifulSoup(open(file), 'xml')
            # find ground_truth file
            ground_truth = BeautifulSoup(open(file), 'xml')
            self.__citation_correction(ground_truth, bs)
            file = open("SOMETHING.xml", "wb")
            file.write(bs.prettify().encode('utf-8'))

if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))

    scoap3_xmls = directory + '/../training/hindawi_scoap_xmls/'
    input_directory = '/home/joseph/Desktop/grobid/grobid-trainer/resources/dataset/reference-segmenter/corpus/tei/'
    output_directory = directory + \
    '/../grobid/grobid-trainer/resources/dataset/reference-segmenter/corpus/tei/'

    val = Validator(ground_truth_directory = scoap3_xmls, 
                    bs_directory = input_directory,
                    output_directory = output_directory)
    val.reference_segmenter_validation()