
import sys, json, MySQLdb

from src.utils import logger, getCliHelpText, parseOptions, parseYamlFile
from src.data_gen import DataGen


if __name__ == "__main__":
    try:
        inputFile = parseOptions(sys.argv[1:])
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)
    inputConfig = parseYamlFile(inputFile)

    if inputConfig["engine"] == "mysql":
        from src.schema_builders.mysql import MysqlSchemaBuilder as SchemaBuilder
        from src.writers.mysql import MysqlWriter as Writer
        from src.contexts.mysql import MysqlContext as Context
        conn = MySQLdb.connect(
            inputConfig["host"],
            inputConfig["user"],
            inputConfig["password"],
            inputConfig["database"],
            inputConfig["port"]
        )
        ctx = Context(conn, inputConfig)

    else:
        logger.error("Engine - {} not supported".format(inputConfig["engine"]))
        sys.exit(1)

    orderInfo, schemaForDatagen = SchemaBuilder(ctx).getSchemaForDataGen()
    logger.debug("Schema for data generation:\n{}".format(json.dumps(schemaForDatagen)))
    logger.debug("Will be worked in order:\n{}".format(json.dumps(orderInfo)))
    writer = Writer(ctx)
    dataGen = DataGen(ctx)
    for results in dataGen.generate(schemaForDatagen, orderInfo):
        logger.info("Writing {} documents into {}..".format(len(results["docs"]), results["table"]))
        writer.doBulkWrite(results["table"], results["docs"])
    logger.info("Finally, Done with it!")
