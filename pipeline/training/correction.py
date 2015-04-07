import json
import re
from os import environ, path
from bs4 import BeautifulSoup

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

class Validator():
    """
    Class for validating training set produced by grobid
    """
    def __init__(self, ground_truth_directory, bs_directory):
        self.ground_truth_directory = ground_truth_directory
        self.bs_directory = bs_directory
    """
    Correct reference_segmenter TEI
    """
    def reference_segmenter_correction(self, ground_truth, bs):
        gt_ref = ground_truth.back.find('ref-list').find('ref')
        bs_ref = bs.find('listBibl').find('bibl')

        while gt_ref is not None:
            # print gt_ref.label.string, bs_ref
            if bs_ref.label is None:
                frag = bs_ref.text
                prev_bs_ref = bs_ref.find_previous('bibl')
                prev_frag = prev_bs_ref.label.next_sibling.string
                prev_bs_ref.label.next_sibling.string = prev_frag + frag
                bs_ref.extract()
                bs_ref = prev_bs_ref
                gt_ref = gt_ref.find_previous('ref')
                print bs_ref
            elif ("[" + gt_ref.label.string + "]") != bs_ref.label.string:
                bs_ref = bs_ref.find_previous('bibl')
                if bs_ref.text.find("[" + gt_ref.label.string + "]") >= 0:
                    # Split fragment around correct delimeter
                    split = bs_ref.label.next_sibling.string. \
                            split("[" + gt_ref.label.string + "]")
                    # Construct new bibl and insert
                    bibl_tag = bs.new_tag('bibl')
                    label_tag = bs.new_tag('label')
                    label_tag.string = "[" + gt_ref.label.string + "]"
                    bibl_tag.insert(0, label_tag)
                    bibl_tag.insert(1, split[1])
                    bs_ref.insert_after(bibl_tag)
                    # Correct previous bibl
                    bs_ref.label.next_sibling.replaceWith(split[0])
                    bs_ref = bs_ref.findNext('bibl')
                else: # merge previous and current
                    next_bs_ref = bs_ref.findNext('bibl')
                    next_frag = next_bs_ref.label.string + \
                                next_bs_ref.label.next_sibling.string
                    prev_frag = bs_ref.label.next_sibling.string
                    bs_ref.label.next_sibling. \
                                 replaceWith(prev_frag + next_frag)
                    next_bs_ref.extract()
                    gt_ref = gt_ref.find_previous('ref')
            else:
                gt_ref = gt_ref.findNext('ref')
                bs_ref = bs_ref.findNext('bibl')
        return bs
    """
    Correct directory of reference_segmenter training files
    """
    def reference_segmenter_validation(self):
        for file in bs_directory:
            bs = BeautifulSoup(open(file))
            # find ground_truth file
            ground_truth = BeautifulSoup(open(file))
            correction = self.__reference_segmenter_correction(ground_truth, bs)
            file = open("SOMETHING.xml", "wb")
            file.write(bs.prettify().encode('utf-8'))
    """
    Correct citation training TEI file
    """
    def __citation_correction(self):
        pass
    """
    Correct directory of citation training files
    """
    def citation_validation(self):
        pass

if __name__ == '__main__':
    # directory = path.dirname(path.realpath(__file__))

    # scoap3_xmls = directory + '../../training/hindawi_scoap_xmls'
    # grobid_output = directory + '../../grobid/output'
    # val = Validator(ground_truth_directory = scoap3_xmls, 
    #                 bs_directory = grobid_output)
    # val.reference_segmenter_validation()

    val = Validator("", "")
    bs = BeautifulSoup(open('987.training.referenceSegmenter.tei.xml'), 'xml')
    # find ground_truth file
    ground_truth = BeautifulSoup(open('987.xml'), 'xml')
    val.reference_segmenter_correction(ground_truth = ground_truth, bs = bs)