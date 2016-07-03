# All contexts must extend this class

from src.seeders import Seeder

class AbstractContext():


    def __init__(self, conn, inputConfig):
        self.conn = conn
        self.inputConfig = inputConfig

        # Create seeder instance
        self.seeder = Seeder()

        # Used as a temp storage of re-usable dicts
        self.cache = {}


    def getConn(self):
        return self.conn


    def getInputConfig(self):
        return self.inputConfig


    def getSeeder(self):
        return self.seeder


    # --------------------
    # Methods for self.cache operations
    def getCacheKey(self, key):
        return self.cache.get(key, None)


    def setCacheKey(self, key, val):
        self.cache[key] = val

        return self


    def emptyCache(self):
        self.cache = {}

        return self

    # --------------------
