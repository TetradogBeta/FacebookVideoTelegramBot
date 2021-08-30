

class Stream:
    def __init__(self,stream,buffer=1024):
        self.Stream=stream;
        self.Buffer=int(buffer);
        self.Total=int(self.Stream.headers['Content-Length']);##quizás los archivos fa diferente
    
    def iter_content(self,blockSize=None):
        if blockSize is None:
            blockSize=self.Buffer;
        blockSize=int(blockSize);
        return self.Stream.iter_content(blockSize);

###de momento no se como leen los archivos pero la idea es que de igual :D
    def read(self):
         return bytearray(self.iter_content(self.Total));

    def Close(self):
        self.Stream.close();
    
    

