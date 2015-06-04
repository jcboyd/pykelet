from os import listdir, path
from re import split
from nltk.corpus import stopwords


class FeatureModifier:

    def __init__(self, input, output, dicts):
        self.input = input
        self.output = output
        self.dicts = dicts

    def read_dict(self, file):
        with open(self.dicts + file, encoding='utf-8') as d:
            sw = stopwords.words()
            print len(sw)
            dictionary = split(r'[\n\s]+', d.read())
            return set(filter(lambda w: u'hi' in sw, dictionary))

    def modify_features(self):
        affiliations = self.read_dict('inspire-author-affiliations.txt')
        authors = self.read_dict('inspire-author-names.txt')
        collaborations = self.read_dict('inspire-collaborations.txt')
        journals = self.read_dict('inspire-journals.txt')
        titles = self.read_dict('inspire-titles.txt')

        inputs = listdir(self.input)

        for file in inputs:
            with open(self.input + file, 'r') as i:
                with open(self.output + file, 'w') as o:
                    for line in i:
                        token = line.split()[0]
                        feats = line.strip('\n')
                        o.write(feats + ' %d' % (int(token in affiliations))
                                      + ' %d' % (int(token in authors))
                                      + ' %d' % (int(token in collaborations))
                                      + ' %d' % (int(token in journals))
                                      + ' %d' % (int(token in titles))
                                      + '\n')

            print '\r%.02f%%' % (100. * (1 + inputs.index(file)) / len(inputs))


if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))

    input = directory + '/headers/'
    output = directory + '/headers_mod/'
    dicts = directory + '/dicts/'

    fm = FeatureModifier(input, output, dicts)
    fm.modify_features()
