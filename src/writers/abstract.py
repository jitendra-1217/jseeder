# All writers must extend this class

class AbstractWriter():


    def __init__(self, ctx):
        self.ctx = ctx


    # Does bulk writing of documents to the engine
    def doBulkWrite(self):
        raise NotImplementedError
