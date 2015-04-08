from os import environ, path

class GrobidTrainer():
    """
    Wrapper class for calling grobid core
    """
    def __init__(self, classpath, grobid_home, model):
        self.grobid_home = grobid_home
        self.model = model

        environ['CLASSPATH'] = classpath

        from jnius import autoclass # $ pip install cython jnius
        self.bootloader = autoclass('com.simontuffs.onejar.Boot')
    """
    Wrapper for training model
    """
    def train(self):
        self.bootloader.main(['0', self.model,
                              '-gH', self.grobid_home])
    """
    Wrapper for evaluating model
    """
    def evaluate(self):
        self.bootloader.main(['1', self.model,
                              '-gH', self.grobid_home])
    """
    Wrapper for training and evaluating model
    """
    def trainAndEvaluate(self, split):
        self.bootloader.main(['2', self.model,
                              '-gH', self.grobid_home,
                              '-s', split])

class GrobidCore():
    """
    Wrapper class for calling grobid core
    """
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

        from jnius import autoclass # $ pip install cython jnius
        self.bootloader = autoclass('com.simontuffs.onejar.Boot')
    """
    Wrapper for calling processHeader
    """
    def processHeader(self):
        self.bootloader.main(['-gH', self.grobid_home,
                              '-gP', self.grobid_properties,
                              '-dIn', self.grobid_input,
                              '-dOut', self.grobid_output,
                              '-exe', 'processHeader'])
    """
    Wrapper for calling processFullText
    """
    def processFullText(self):
        pass
    """
    Wrapper for calling processDate
    """
    def processDate(self):
        pass
    """
    Wrapper for calling processAuthorsHeader
    """
    def processAuthorsHeader(self):
        pass
        """
    Wrapper for calling processAuthorsCitation
    """
    def processAuthorsCitation(self):
        pass
    """
    Wrapper for calling processAffiliation
    """
    def processAffiliation(self):
        pass
    """
    Wrapper for calling processRawReference
    """
    def processRawReference(self):
        pass
    """
    Wrapper for calling processReferences
    """
    def processReferences(self):
        self.bootloader.main(['-gH', self.grobid_home,
                              '-gP', self.grobid_properties,
                              '-dIn', self.grobid_input,
                              '-dOut', self.grobid_output,
                              '-exe', 'processReferences'])
    """
    Wrapper for calling processReferences
    """
    def createTrainingReferenceSegmentation(self):
        self.bootloader.main(['-gH', self.grobid_home,
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

    classpath_core = directory + '/../grobid/grobid-core.jar'
    grobid_core = GrobidCore(classpath = classpath_core,
                             grobid_home = exitgrobid_home,
                             grobid_properties = grobid_properties,
                             grobid_input = grobid_input,
                             grobid_output = grobid_output)
    grobid_core.createTrainingReferenceSegmentation()

    classpath_trainer = directory + '/../grobid/grobid-trainer.jar'
    model = 'reference-segmenter'
    grobid_trainer = GrobidTrainer(classpath = classpath_trainer,
                                   grobid_home = grobid_home,
                                   model = model)
    grobid_trainer.train()