
import MySQLdb
from src.contexts.abstract import AbstractContext

class MysqlContext(AbstractContext):


    def __init__(self, conn, inputConfig):
        AbstractContext.__init__(self, conn, inputConfig)
        self.seeder.setUpMySQLSeeders(self.getConn())
        self.cursor = self.getConn().cursor(cursorclass=MySQLdb.cursors.DictCursor)


    def getCursor(self):
        return self.cursor
