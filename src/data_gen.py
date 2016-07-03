
from src.utils import logger, cache


class DataGen():

    # Class constants
    kDocBatchCount = 1000


    def __init__(self, ctx):
        self.ctx = ctx

        self.seeder = self.ctx.getSeeder()


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

        inputConfig = self.ctx.getInputConfig()
        numOfDocsToGen = inputConfig["includeTables"][table]["seedSize"]
        logger.info("Will generate {} documents for {}..".format(numOfDocsToGen, table))

        # Following code does following:
        # - Creates given "numbers of" documents "in batch" usign given "schema of table and it's fields"
        # - Fields schema has info on what seeder to call
        # - Finally it returns the list of dict
        numOfDocsWorked = 0
        diff = numOfDocsToGen - numOfDocsWorked
        while diff > 0:
            localBatchCount = DataGen.kDocBatchCount if DataGen.kDocBatchCount < diff else diff
            numOfDocsWorked += localBatchCount
            diff = numOfDocsToGen - numOfDocsWorked
            docs = []
            while localBatchCount > 0:
                doc = {}
                for f, fSchema in fieldsSchema.items():
                    doc[f] = self.seeder.callSeederFunc(fSchema["seeder"], fSchema["seederArgs"])
                docs.append(doc)
                localBatchCount -= 1
            yield {"docs": docs, "table": table}
        # Emptying cache after every table seed..
        cache.emptyCache()
