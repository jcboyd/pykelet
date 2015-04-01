from os import environ
from import jnius

os.environ['CLASSPATH'] = "path/to/your.jar"

javaclass = autoclass('path.to.your.class')
javaclass.main([])
