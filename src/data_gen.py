
from src.utils import logger, cache


class DataGen():

    kDocBatchCount = 1000


    def __init__(self, ctx):
        self.ctx = ctx
        self.seeder = self.ctx.getSeeder()


    def generate(self, schemaForDatagen, orderInfo=False):
        # (1) Yields documents with key: value pairs to be written into the calling engine (mysql/mongodb etc..)
        tables = [orderInfo[k] for k in sorted(orderInfo.keys(), reverse=True)] if orderInfo else schemaForDatagen.keys()
        for table in tables:
            for d in self._workForTable(table, schemaForDatagen[table]):
                yield d


    def _workForTable(self, table, fieldsSchema):
        inputConfig = self.ctx.getInputConfig()
        numOfDocsToGen = inputConfig["includeTables"][table]["seedSize"]
        logger.info("Will generate {} documents for {}..".format(numOfDocsToGen, table))

        # Following code does following:
        # (1) Creates given "numbers of" documents "in batch" usign given "schema of table and it's fields"
        # (2) Fields schema has info on what seeder to call
        # (3) Finally it returns the list of dict
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
        cache.emptyCache()
