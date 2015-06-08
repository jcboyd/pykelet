from os import path
from subprocess import call


class GrobidTrainer():

    """Wrapper class for calling grobid core."""

    def __init__(self, classpath, grobid_home):
        self.classpath = classpath
        self.grobid_home = grobid_home

    def train(self, model):
        """Wrapper for training model."""
        call(['java', '-Xmx1024m', '-jar', self.classpath,
              '0', model, '-gH', self.grobid_home])

    def evaluate(self, model):
        """Wrapper for evaluating model."""
        call(['java', '-Xmx1024m', '-jar', self.classpath,
              '1', model, '-gH', self.grobid_home])

    def trainAndEvaluate(self, model, split):
        """Wrapper for training and evaluating model."""
        call(['java', '-Xmx1024m', '-jar', self.classpath,
              '2', model, '-gH', self.grobid_home, '-s', split])


class GrobidCore():

    """Wrapper class for calling grobid core."""

    def __init__(self,
                 classpath,
                 grobid_home,
                 grobid_properties,
                 grobid_input,
                 grobid_output):
        self.classpath = classpath
        self.grobid_home = grobid_home
        self.grobid_properties = grobid_properties
        self.grobid_input = grobid_input
        self.grobid_output = grobid_output

    def processHeader(self):
        """Wrapper for calling processHeader."""
        call(['java', '-Xmx1024m',
              '-jar', self.classpath,
              '-gH', self.grobid_home,
              '-gP', self.grobid_properties,
              '-dIn', self.grobid_input,
              '-dOut', self.grobid_output,
              '-exe', 'processHeader'])

    def processFullText(self):
        """Wrapper for calling processFullText."""
        pass

    def processDate(self):
        """Wrapper for calling processDate."""
        pass

    def processAuthorsHeader(self):
        """Wrapper for calling processAuthorsHeader."""
        pass

    def processAuthorsCitation(self):
        """Wrapper for calling processAuthorsCitation."""
        pass

    def processAffiliation(self):
        """Wrapper for calling processAffiliation."""
        pass

    def processRawReference(self):
        """Wrapper for calling processRawReference."""
        pass

    def processReferences(self):
        """Wrapper for calling processReferences."""
        call(['java', '-Xmx1024m',
              '-jar', self.classpath,
              '-gH', self.grobid_home,
              '-gP', self.grobid_properties,
              '-dIn', self.grobid_input,
              '-dOut', self.grobid_output,
              '-exe', 'processReferences'])

    def createTrainingReferenceSegmentation(self):
        """Wrapper for calling processReferences."""
        call(['java', '-Xmx1024m',
              '-jar', self.classpath,
              '-gH', self.grobid_home,
              '-gP', self.grobid_properties,
              '-dIn', self.grobid_input,
              '-dOut', self.grobid_output,
              '-exe', 'createTrainingReferenceSegmentation'])

if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))

    grobid_home = directory + '/../grobid/grobid-home'
    grobid_properties = grobid_home + '/config/grobid.properties'
    grobid_input = directory + '/../grobid/input'
    grobid_output = directory + '/../grobid/output'

    classpath_core = directory + '/../grobid/grobid-core/target/ \
                                  grobid-core-0.3.4-SNAPSHOT.jar'
    grobid_core = GrobidCore(classpath=classpath_core,
                             grobid_home=grobid_home,
                             grobid_properties=grobid_properties,
                             grobid_input=grobid_input,
                             grobid_output=grobid_output)
    grobid_core.createTrainingReferenceSegmentation()

    classpath_trainer = directory + '/../grobid/grobid-trainer/target/ \
                                    grobid-trainer-0.3.4-SNAPSHOT.jar'
    model = 'reference-segmenter'
    grobid_trainer = GrobidTrainer(classpath=classpath_trainer,
                                   grobid_home=grobid_home)
    grobid_trainer.train(model)
