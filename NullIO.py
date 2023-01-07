from io import StringIO

class NullIO(StringIO):
    def write(self, txt):
       pass