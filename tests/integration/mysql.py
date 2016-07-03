
import unittest, MySQLdb, json

from src.schema_builders.mysql import MysqlSchemaBuilder as SchemaBuilder
from src.writers.mysql import MysqlWriter as Writer
from src.contexts.mysql import MysqlContext as Context
from src.utils import logger
from src.data_gen import DataGen

class MysqlIntegrationTest(unittest.TestCase):

    conn        = None
    inputConfig = None
    cursor      = None

    @classmethod
    def setUpClass(self):

        logger.debug("Setting up class..")

        self.inputConfig = {
            'engine':        'mysql',
            'host':          'localhost',
            'user':          'jseeder',
            'database':      'jseeder',
            'password':      'jseeder',
            'port':          3306,
            'includeTables': {
                'users': {
                    'seedSize': 100
                }
            }
        }
        logger.info("Using following input config:\n{}".format(json.dumps(self.inputConfig)))

        # At this point ensure above db is created already
        self.conn = MySQLdb.connect(
            self.inputConfig["host"],
            self.inputConfig["user"],
            self.inputConfig["password"],
            self.inputConfig["database"],
            self.inputConfig["port"]
        )

        logger.info("Creating required test tables..")
        # Create test tables
        self.cursor = self.conn.cursor()
        sql = """CREATE TABLE users (
                id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                first_name  VARCHAR(20) NOT NULL,
                last_name  VARCHAR(20))"""
        self.cursor.execute(sql)


    def testMysqlSeeder(self):

        logger.info("Initializing mysql integration testing components..")

        ctx = Context(self.conn, self.inputConfig)
        orderInfo, schemaForDatagen = SchemaBuilder(ctx).getSchemaForDataGen()
        logger.debug("Schema for data generation:\n{}".format(json.dumps(schemaForDatagen)))
        logger.debug("Will be worked in order:\n{}".format(json.dumps(orderInfo)))

        writer = Writer(ctx)
        dataGen = DataGen(ctx)

        for results in dataGen.generate(schemaForDatagen, orderInfo):
            logger.info("Writing {} documents into {}..".format(len(results["docs"]), results["table"]))
            writer.doBulkWrite(results["table"], results["docs"])

        logger.info("Finally, Done with it!")


    @classmethod
    def tearDownClass(self):
        logger.debug("Tearing down class..")

        logger.info("Droping all tests tables..")
        sql = "DROP TABLE users"
        self.cursor.execute(sql)