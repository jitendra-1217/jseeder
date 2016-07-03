# All schema builder must extend this class

class AbstractSchemaBuilder():


    def __init__(self, ctx):
        self.ctx = ctx


    def getCtx(self):
        return self.ctx


    # Get schema to be used by data generator
    def getSchemaForDataGen(self):
        raise NotImplementedError
