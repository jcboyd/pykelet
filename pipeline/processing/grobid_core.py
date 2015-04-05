from os import environ, path

class GrobidTrainer():
    """
    Wrapper class for calling grobid core
    """
    def __init__(self):
        pass
    """
    Wrapper class for calling grobid core
    """
    def createTraining():
        pass

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

        from jnius import autoclass #$ pip install cython jnius
        self.bootloader = autoclass('com.simontuffs.onejar.Boot')
    """
    Wrapper for calling processHeader
    """
    def processHeader(self):
        self.bootloader.main(['-gH', self.grobid_home,
                              '-gP', self.grobid_properties,
                              '-dIn', grobid_input,
                              '-dOut', grobid_output,
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
        pass

if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))
    classpath = directory + '/../grobid/grobid-core-0.3.3-SNAPSHOT.one-jar.jar'
    grobid_home = '/home/joseph/Documents/grobid/grobid-home/'
    grobid_properties = grobid_home + '/config/grobid.properties'
    grobid_input = directory + '/../grobid/input'
    grobid_output = directory + '/../grobid/output'
    grobid = GrobidCore(classpath = classpath,
                        grobid_home = grobid_home,
                        grobid_properties = grobid_properties,
                        grobid_input = grobid_input,
                        grobid_output = grobid_output)
    grobid.processHeader()