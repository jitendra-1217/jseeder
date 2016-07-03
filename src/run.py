
import sys, json, MySQLdb

from src.utils import logger, getCliHelpText, parseOptions, parseYamlFile
from src.data_gen import DataGen

if __name__ == "__main__":

    inputFile = parseOptions(sys.argv[1:])
    inputConfig = parseYamlFile(inputFile)

    # -------------------- TODO 1
    # Validate inputConfig

    if inputConfig["engine"] == "mysql":

        from src.schema_builders.mysql import MysqlSchemaBuilder as SchemaBuilder
        from src.writers.mysql import MysqlWriter as Writer
        from src.contexts.mysql import MysqlContext as Context

        # Init variables for context object
        conn = MySQLdb.connect(inputConfig["host"], inputConfig["user"], inputConfig["password"], inputConfig["database"], inputConfig["port"])

        ctx = Context(conn, inputConfig)

    else:

        logger.error("Engine - {} not supported".format(inputConfig["engine"]))
        sys.exit(1)


    # --------------------
    # Absctract code for all engines (mysql, postgres, mongodb etc.)

    # Steps:
    #     1. Get schema for data generation using config received from input file
    #     2. Pass above schema to DataGen
    #     3. DataGen does following for every table in config:
    #         1. Use default or **custom seeders to prepare fake data for all keys in the worked upon table
    #         2. Yield batch of documents containing document with key & value.
    #     4. The batch data from DataGen to be passed to writer

    schemaForDatagen = SchemaBuilder(ctx).getSchemaForDataGen()
    logger.debug("Schema for data generation:\n{}".format(json.dumps(schemaForDatagen)))

    writer = Writer(ctx)
    dataGen = DataGen(ctx)

    for results in dataGen.generate(schemaForDatagen):
        logger.info("Writing {} documents into {}..".format(len(results["docs"]), results["table"]))
        writer.doBulkWrite(results["table"], results["docs"])

    logger.info("Finally, Done with it!")
