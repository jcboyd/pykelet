from os import environ, path


class GrobidTrainer():

    """Wrapper class for calling grobid core."""

    def __init__(self, classpath, grobid_home):
        self.grobid_home = grobid_home

        environ['CLASSPATH'] = classpath
        print classpath

        from jnius import autoclass  # $ pip install cython jnius
        self.trainer = autoclass('org.grobid.trainer.TrainerRunner')

    def train(self, model):
        """Wrapper for training model."""
        self.trainer.main(['0', model, '-gH', self.grobid_home])

    def evaluate(self, model, log_path):
        """Wrapper for evaluating model."""
        self.trainer.main(['1', model,
                           '-gH', self.grobid_home,
                           '-l', log_path])

    def trainAndEvaluate(self, model, split, log_path):
        """Wrapper for training and evaluating model."""
        self.trainer.main(['2', model,
                          '-gH', self.grobid_home,
                          '-s', split,
                          '-l', log_path])


class GrobidCore():

    """Wrapper class for calling grobid core."""

    def __init__(self,
                 classpath,
                 grobid_home,
                 grobid_properties,
                 grobid_input,
                 grobid_output):
        self.grobid_home = grobid_home
        self.grobid_properties = grobid_properties
        self.grobid_input = grobid_input
        self.grobid_output = grobid_output

        environ['CLASSPATH'] = classpath

        from jnius import autoclass  # $ pip install cython jnius
        self.core = autoclass('org.grobid.core.main.batch.GrobidMain')

    def processHeader(self):
        """Wrapper for calling processHeader."""
        self.core.main(['-gH', self.grobid_home,
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
        self.core.main(['-gH', self.grobid_home,
                        '-gP', self.grobid_properties,
                        '-dIn', self.grobid_input,
                        '-dOut', self.grobid_output,
                        '-exe', 'processReferences'])

    def createTrainingReferenceSegmentation(self):
        """Wrapper for calling processReferences."""
        self.core.main(['-gH', self.grobid_home,
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
