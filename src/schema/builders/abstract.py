# All schema builder must extend this class

class AbstractSchemaBuilder():


    def __init__(self, ctx):
        self.ctx = ctx


    # Get schema to be used by data generator
    def getSchemaForDatagen(self):
        raise NotImplementedError
