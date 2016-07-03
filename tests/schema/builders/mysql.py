
import unittest
import MySQLdb
import json

from src.utils import logger, parseYamlFile
from src.schema_builders.mysql import MysqlSchemaBuilder as SchemaBuilder
from src.writers.mysql import MysqlWriter as Writer
from src.contexts.mysql import MysqlContext as Context

class MysqlSchemaBuilderTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.debug("Setting up class..")

    @classmethod
    def tearDownClass(self):
        logger.debug("Tearing down class..")

    def testMysqlSchemaBuilder(self):

        inputConfig = parseYamlFile("/home/vagrant/jseeder/src/configs/input/sample.yaml")
        # Init variables for context object
        conn = MySQLdb.connect(inputConfig["host"], inputConfig["user"], inputConfig["password"], inputConfig["database"], inputConfig["port"])
        ctx = Context(conn, inputConfig)
        msb = SchemaBuilder(ctx)
        tOrder, tSchema = msb.getSchemaForDataGen()
        logger.debug(tOrder)
        logger.debug(json.dumps(tSchema))
