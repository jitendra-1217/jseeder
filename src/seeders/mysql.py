
from src.utils import cache, logger

import random, MySQLdb


class MySQL():


    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)


    def seedFromTableRef(self, table, field, inSerial=True, offset=0, limit=10000):
        cacheKey = "seedFromTableRef___{}___{}".format(table, field)
        hit      = cache.getCacheKey(cacheKey)
        if not hit:
            logger.debug("Queries into table for {}".format(cacheKey))
            self.cursor.execute("SELECT {} FROM {} LIMIT {}, {}".format(field, table, offset, limit))
            hit = [result[field] for result in self.cursor.fetchall()]
            cache.setCacheKey(cacheKey, hit)
        # TODO (3): Following should go in some utility file
        #           Used in seeders/j.py also
        if not inSerial:
            return random.choice(hit)
        k = "MySQL__seedFromTableRef__{}__{}".format(table, field)
        i = cache.getCacheKey(k, 0)
        cache.setCacheKey(k, i + 1)
        hitLen = len(hit)

        return hit[i%hitLen]
