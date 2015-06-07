from os import listdir, path
from sys import stdout
from re import split
from nltk import corpus


class FeatureModifier:

    def __init__(self, inputs, outputs, dicts):
        self.inputs = inputs
        self.outputs = outputs
        self.dicts = dicts

    def read_dict(self, f):
        print 'Reading %s...' % (f)
        with open(self.dicts + f) as d:
            return set(split(r'[\n\s]+', d.read()))

    def modify_features(self):
        affiliations = self.read_dict('inspire-author-affiliations.txt')
        authors = self.read_dict('inspire-author-names.txt')
        collaborations = self.read_dict('inspire-collaborations.txt')
        journals = self.read_dict('inspire-journals.txt')
        titles = self.read_dict('inspire-titles.txt')
        stop_words = set(corpus.stopwords.words())

        inputs = listdir(self.inputs)

        print 'Modifying features...'

        for f in inputs:
            with open(self.inputs + f, 'r') as i:
                with open(self.outputs + f, 'w') as o:
                    for feats in filter(bool, [line.strip() for line in i]):
                        token = feats.split()[0]
                        o.write(feats + ' %d' % (int(token in affiliations))
                                      + ' %d' % (int(token in authors))
                                      + ' %d' % (int(token in collaborations))
                                      + ' %d' % (int(token in journals))
                                      + ' %d' % (int(token in titles))
                                      + ' %d' % (int(token in stop_words))
                                      + '\n')

            print '\r%.02f%%' % (100. * (1 + inputs.index(f)) / len(inputs)),
            stdout.flush()

        print '\rComplete!'


if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))

    inputs = directory + '/headers/'
    outputs = directory + '/headers_mods/'
    dicts = directory + '/dicts/'

    fm = FeatureModifier(inputs, outputs, dicts)
    fm.modify_features()

    # directory = '/home/joseph/Desktop/batches/H_HappC/grobid-trainer/resources/dataset/header/evaluation'
    # inputs = directory + '/headers (copy)/'
    # outputs = directory + '/headers/'
    # dicts = '/home/joseph/Desktop/dicts/'
