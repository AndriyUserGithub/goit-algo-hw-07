class FileManager:
    def __init__(self, path, mode = "r", encoding = "utf-8"):
        self.file = None
        self.fopen = False
        self.path = path
        self.mode = mode
        self.encoding = encoding

    def __enter__(self):
        self.file = open(self.path, self.mode, encoding = self.encoding)
        self.fopen = True
        return self.file
    
    def __exit__(self, *args):
        if self.fopend:
            self.file.close()
        self.fopen = False


        