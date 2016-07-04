
from src.schema_builders.abstract import AbstractSchemaBuilder

import re

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
    def getSchemaForDataGen(self):

        ctx = self.getCtx()
        cursor = ctx.getCursor()
        inputConfig = ctx.getInputConfig()

        return self._getOrderedByDependency({t: self._getSchemaForTable(cursor, inputConfig["database"], t, tConfig) for t, tConfig in inputConfig["includeTables"].items()})



    # --------------------
    # Private methods (Meant to be used inside this class only)


    def _getSchemaForTable(self, cursor, database, t, tConfig):

        tSchema = {}

        # Get all table fields with their meta
        cursor.execute("DESCRIBE {}".format(t))
        results = cursor.fetchall()
        for result in results:
            # Ignore field cases..
            if result["Extra"] == "auto_increment":
                continue
            if result["Field"] in tConfig.get("excludeFields", []):
                continue

            defSeeder, defSeederArgs = self._mapSeederByMysqlDatatype(result["Type"])
            tSchema[result["Field"]] = {
                # Assign default seeder func mapped via mysql data types
                "seeder":       defSeeder,
                "seederArgs":   defSeederArgs,
                "dependencies": {}
            }
            if result["Field"] in tConfig.get("includeFields", []):
                tSchema[result["Field"]].update(tConfig["includeFields"][result["Field"]])
            elif tConfig.get("inclusionPolicy", "none") == "none":
                del(tSchema[result["Field"]])

        self.fixSeederArgs(tSchema, t)

        # Get references and update seeder and other field schema attrs
        cursor.execute("SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(database, t))
        results = cursor.fetchall()
        for result in results:
            # Ignore if the column is not already in schema
            if result["COLUMN_NAME"] not in tSchema:
                continue
            # Update seeder, seederArgs and dependencies
            tSchema[result["COLUMN_NAME"]]["dependencies"] = {
                "table": result["REFERENCED_TABLE_NAME"],
                "field": result["REFERENCED_COLUMN_NAME"]
            }
            tSchema[result["COLUMN_NAME"]]["seeder"] = "mysql.seedFromTableRef"
            tSchema[result["COLUMN_NAME"]]["seederArgs"] = [result["REFERENCED_TABLE_NAME"], result["REFERENCED_COLUMN_NAME"]]

        return tSchema


    # BUG: Self referencing tables leading to infinite loop while resolving dependencies
    def _getOrderedByDependency(self, tSchema):

        tOrder = {}
        includeTables = tSchema.keys()
        tMap = {t: False for t in includeTables}
        tLen = len(includeTables)

        while tLen > 0:
            for t in includeTables:
                td = [v["dependencies"]["table"] for f, v in tSchema[t].items() if "table" in v["dependencies"]]
                if len([k for k in td if k in tMap and tMap[k] == False]) == 0 and tMap[t] == False:
                    tMap[t] = True
                    tOrder[tLen] = t
                    tLen -= 1

        return (tOrder, tSchema)


    def _mapSeederByMysqlDatatype(self, type):

        # Char type fields
        m = re.search("(.*?)char\((.+?)\)", type)
        if m:
            return ("fake.text", [int(m.group(2))])

        # Int type fields
        m = re.search("(.*?)int\((.+?)\)", type)
        if m:
            t = m.group(1)
            if t == "tiny":
                intMax = 1
            elif t == "small":
                intMax = 32767
            elif t == "medium":
                intMax = 8388607
            elif t == "": # i.e. int
                intMax = 2147483647
            elif t == "big":
                intMax = 9223372036854775807
            else:
                intMax = 1

            return ("fake.random_int", [1, intMax])

        # Other regex might follow..

        # Otherwise returning something which will throw errors later.. :(
        # OR, Better should throw error here only
        # return (type, [])
        raise Exception("No mapped seeder found for mysql data type: {}".format(type))
