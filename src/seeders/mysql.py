
from src.utils import cache, logger

import random, MySQLdb


class MySQL():


    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)


    def seedFromTableRef(self, table, field):
        cacheKey = "seedFromTableRef___{}___{}".format(table, field)
        hit      = cache.getCacheKey(cacheKey)
        if not hit:
            logger.debug("Queries into table for {}".format(cacheKey))
            self.cursor.execute("SELECT {} FROM {}".format(field, table))
            hit = [result[field] for result in self.cursor.fetchall()]
            cache.setCacheKey(cacheKey, hit)

        return random.choice(hit)
