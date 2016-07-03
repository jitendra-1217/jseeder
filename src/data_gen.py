
# Notes:
# - While calling any seeder util/func/method, if it requires pass the self.ctx object
#   for it to use.
# - **Try cleaning ctx.cache after every table is processed

from src.utils import logger
from src.seeders import callSeederFunc

class DataGen():

    # Class constants
    kDocBatchCount = 1000

    def __init__(self, ctx):
        self.ctx = ctx


    # From run.py >
    # 3. DataGen does following for every table in config:
    #     1. Use default or **custom seeders to prepare fake data for all keys in the worked upon table
    #     2. Yield batch of documents containing document with key & value.
    def generate(self, schemaForDatagen, orderInfo=False):

        tables = [orderInfo[k] for k in sorted(orderInfo.keys(), reverse=True)] if orderInfo else schemaForDatagen.keys()
        for table in tables:
            for d in self._workForTable(table, schemaForDatagen[table]):
                yield d


    def _workForTable(self, table, fieldsSchema):

        logger.debug("Will start generating data for: {}".format(table))
        inputConfig = self.ctx.getInputConfig()
        numOfDocsToGen = inputConfig["includeTables"][table]["seedSize"]
        logger.debug("Will generate {} number of documents".format(numOfDocsToGen))

        numOfDocsWorked = 0
        d = numOfDocsToGen - numOfDocsWorked
        while d > 0:
            c = DataGen.kDocBatchCount if DataGen.kDocBatchCount < d else d
            numOfDocsWorked += c
            d = numOfDocsToGen - numOfDocsWorked
            docs = []
            while c > 0:
                doc = {}
                for f, fSchema in fieldsSchema.items():
                    doc[f] = callSeederFunc(fSchema["seeder"], fSchema["seederArgs"])
                docs.append(doc)
                c -= 1
            yield {"docs": docs, "table": table}
