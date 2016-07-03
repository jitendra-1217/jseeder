# All contexts must extend this class

from src.seeders import Seeder

class AbstractContext():


    def __init__(self, conn, inputConfig):
        self.conn = conn
        self.inputConfig = inputConfig

        # Create seeder instance
        self.seeder = Seeder()


    def getConn(self):
        return self.conn


    def getInputConfig(self):
        return self.inputConfig


    def getSeeder(self):
        return self.seeder
