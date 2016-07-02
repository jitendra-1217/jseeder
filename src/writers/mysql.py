
from src.writers.abstract import AbstractWriter

class MysqlWriter(AbstractWriter):


    def __init__(self, ctx):
        AbstractWriter.__init__(self, ctx)


    def doBulkWrite(self, table, docs):
        pass
