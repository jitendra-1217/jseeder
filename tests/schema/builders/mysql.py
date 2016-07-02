
import unittest
from src.utils import logger

class MysqlSchemaBuilderTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.debug("Setting up class..")

    @classmethod
    def tearDownClass(self):
        logger.debug("Tearing down class..")

    def testMysqlSchemaBuilder(self):
        pass
