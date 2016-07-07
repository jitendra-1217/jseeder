
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
            "engine":        "mysql",
            "host":          "localhost",
            "user":          "jseeder",
            "database":      "jseeder",
            "password":      "jseeder",
            "port":          3306,
            "includeTables": {
                "users": {
                    "seedSize":        10,
                    "excludeFields":   ["middle_name"],
                    "inclusionPolicy": "all", # "all"/"none" - Include all/ none fields, default - "none"
                    "includeFields":   {
                        "first_name": {
                            "seeder":     "j.fromList",
                            "seederArgs":  {
                                "l": ["jitendra", "kumar", "ojha"],
                                "inSerial": True
                            }
                        },
                        "last_name": {
                            "seeder":     "j.fromList",
                            "seederArgs":  {
                                "l": ["jitendra", "kumar", "ojha"],
                                "inSerial": True
                            }
                        },
                        "fav_num": {
                            "seeder":     "j.fromBetween",
                            "seederArgs":  {
                                "i": 0,
                                "j": 3,
                                "inSerial": False
                            }
                        },
                        "city_id": {
                            "seederArgs": {
                                "inSerial": True,
                                "offset":   3,
                                "limit":    5
                            }
                        }
                    }
                },
                "cities": {
                    "seedSize":        10,
                    "inclusionPolicy": "all",
                    "includeFields":   {
                        "name": {
                            "seeder": "j.fromList",
                            "seederArgs":  {
                                "l": ["Bangalore", "Patna"],
                                "inSerial": True
                            }
                        }
                    }
                }
            }
        }
        logger.info("Using following input config:\n{}".format(json.dumps(self.inputConfig)))
        self.conn = MySQLdb.connect(
            self.inputConfig["host"],
            self.inputConfig["user"],
            self.inputConfig["password"],
            self.inputConfig["database"],
            self.inputConfig["port"]
        )
        logger.info("Creating required test tables..")
        self.cursor = self.conn.cursor()
        sql = """CREATE TABLE cities (
                id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                name  VARCHAR(20) NOT NULL)"""
        self.cursor.execute(sql)
        sql = """CREATE TABLE users (
                id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                first_name  VARCHAR(20) NOT NULL,
                middle_name VARCHAR(20),
                last_name  VARCHAR(20),
                fav_num INT,
                city_id INT,
                CONSTRAINT fk_users_cities_city_id_id FOREIGN KEY (city_id) REFERENCES cities(id))"""
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
        self.cursor.execute("DROP TABLE users")
        self.cursor.execute("DROP TABLE cities")
