from os import environ, path

class GrobidTrainer():
    
    """Wrapper class for calling grobid core."""

    def __init__(self, classpath, grobid_home, model):
        self.grobid_home = grobid_home
        self.model = model

        environ['CLASSPATH'] = classpath

        from jnius import autoclass # $ pip install cython jnius
        self.bootloader = autoclass('com.simontuffs.onejar.Boot')
    
    def train(self):
        """Wrapper for training model."""
        self.bootloader.main(['0', self.model,
                              '-gH', self.grobid_home])
    
    def evaluate(self):
        """Wrapper for evaluating model."""
        self.bootloader.main(['1', self.model, '-gH', self.grobid_home])

    def trainAndEvaluate(self, split):
        """Wrapper for training and evaluating model."""
        self.bootloader.main(['2', self.model,
                              '-gH', self.grobid_home,
                              '-s', split])

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

        from jnius import autoclass # $ pip install cython jnius
        self.bootloader = autoclass('com.simontuffs.onejar.Boot')
    
    def processHeader(self):
        """Wrapper for calling processHeader."""
        self.bootloader.main(['-gH', self.grobid_home,
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
        self.bootloader.main(['-gH', self.grobid_home,
                              '-gP', self.grobid_properties,
                              '-dIn', self.grobid_input,
                              '-dOut', self.grobid_output,
                              '-exe', 'processReferences'])
    
    def createTrainingReferenceSegmentation(self):
        """Wrapper for calling processReferences."""
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
                             grobid_home = grobid_home,
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