
import unittest

def suite():
    suite = unittest.TestSuite()
    from tests.integration.mysql import MysqlIntegrationTest
    suite.addTests(map(MysqlIntegrationTest, ["testMysqlSeeder"]))

    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
