
from src.writers.abstract import AbstractWriter
from src.utils import tryCatchWrapper, logger


class MysqlWriter(AbstractWriter):


    def __init__(self, ctx):
        AbstractWriter.__init__(self, ctx)


    @tryCatchWrapper
    def doBulkWrite(self, table, docs):
        if len(docs) == 0:
            logger.warnings("No docs to do write")
            return
        # Preparing build insert query, e.g. INSERT INTO users (first_name, last_name) VALUES (%(first_name)s, %(last_name)s)
        keys       = docs[0].keys()
        keysRepl   = ", ".join(keys)
        valuesRepl = ", ".join(["%(" + k + ")s" for k in keys])
        sql        = "INSERT INTO {} ({}) VALUES ({})".format(table, keysRepl, valuesRepl)

        self.ctx.getCursor().executemany(sql, docs)
        self.ctx.getConn().commit()
