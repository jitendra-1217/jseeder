# All writers must extend this class

class AbstractWriter():


    def __init__(self, ctx):
        self.ctx = ctx


    def doBulkWrite(self):
        # Does bulk writing of documents to the engine
        raise NotImplementedError
