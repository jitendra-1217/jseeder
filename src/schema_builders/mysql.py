
from src.schema_builders.abstract import AbstractSchemaBuilder

import re

class MysqlSchemaBuilder(AbstractSchemaBuilder):


    def __init__(self, ctx):
        AbstractSchemaBuilder.__init__(self, ctx)


    def getSchemaForDataGen(self):
        # It returns a schema dict which DataGen will use with seeders to generate fake data

        ctx = self.getCtx()
        cursor = ctx.getCursor()
        inputConfig = ctx.getInputConfig()

        return self._getOrderedByDependency({t: self._getSchemaForTable(cursor, inputConfig["database"], t, tConfig) for t, tConfig in inputConfig["includeTables"].items()})



    # --------------------
    # Private methods (Meant to be used inside this class only)


    def _getSchemaForTable(self, cursor, database, t, tConfig):

        tSchema = {}
        includeFields = tConfig.get("includeFields", [])
        # (1) Handle what column to include/exclude and with input seeder args
        # (2) Assingn default seeders for tables' columns
        cursor.execute("DESCRIBE {}".format(t))
        results = cursor.fetchall()
        for result in results:
            if result["Extra"] == "auto_increment" or result["Field"] in tConfig.get("excludeFields", []):
                continue
            if tConfig.get("inclusionPolicy", "none") == "all" or result["Field"] in includeFields:
                tSchema[result["Field"]] = {
                    "seeder":       "",
                    "seederArgs":   {},
                    "dependencies": {}
                }
                if result["Field"] in includeFields and "seeder" not in includeFields[result["Field"]]:
                    defSeeder, defSeederArgs = self._mapSeederByMysqlDatatype(result["Type"])
                    tSchema[result["Field"]].update({
                        "seeder":       defSeeder,
                        "seederArgs":   defSeederArgs
                    })
                if result["Field"] in includeFields:
                    tSchema[result["Field"]].update(includeFields[result["Field"]])
        self.fixSeederArgs(tSchema, t)
        # (3) Find and put the foreign key dependencies for every table's columns
        cursor.execute("SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(database, t))
        results = cursor.fetchall()
        for result in results:
            if result["COLUMN_NAME"] not in tSchema:
                continue
            if result["REFERENCED_TABLE_NAME"] != t:
                tSchema[result["COLUMN_NAME"]]["dependencies"] = {
                    "table": result["REFERENCED_TABLE_NAME"],
                    "field": result["REFERENCED_COLUMN_NAME"]
                }
            # Forcing to use mysql.seedFromTableRef, seederArgs from input config will be used though
            tSchema[result["COLUMN_NAME"]]["seeder"] = "mysql.seedFromTableRef"
            tSchema[result["COLUMN_NAME"]]["seederArgs"].update({"table": result["REFERENCED_TABLE_NAME"], "field": result["REFERENCED_COLUMN_NAME"]})

        return tSchema


    def _getOrderedByDependency(self, tSchema):
        # (1) Resolve foreign key dependencies for doing seeding in proper order,
        #     Returns order dict along with schema

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
        # (1) Returns default seeder for mysql data type

        # Char type fields
        m = re.search("(.*?)char\((.+?)\)", type)
        if m:
            return ("fake.text", [int(m.group(2))])

        # Int type fields (Limits per signed range for safety)
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

            return ("fake.random_int", [0, intMax])

        # TODO (1): Handle following mysql datatypes: datetime, longtext, double, timestamp & year

        raise Exception("No mapped seeder found for mysql data type: {}".format(type))
