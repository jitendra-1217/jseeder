
from src.contexts.abstract import AbstractContext

class MysqlContext(AbstractContext):


    def __init__(self, conn, inputConfig):
        AbstractContext.__init__(self, conn, inputConfig)
