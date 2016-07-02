
from src.schema_builders.abstract import AbstractSchemaBuilder

class MysqlSchemaBuilder(AbstractSchemaBuilder):


    def __init__(self, ctx):
        AbstractSchemaBuilder.__init__(self, ctx)


    # It returns a schema dict which will be used to by DataGen to
    # generate fake data.
    # The schema is expected to have:
    #     - List of tables schema sorted by dependencies.
    #       Eg. If table A references a column in table B, table B would be first to get seeded.
    #       Also how many rows to be seeded and other few metas.
    #     - Each tables have - list of keys with their schema
    #     - Each key schema tells:
    #         - What seeder to use
    #         - And arguments required for the seeder (Must be ensured via code)
    def getSchemaForDatagen(self):
        pass
