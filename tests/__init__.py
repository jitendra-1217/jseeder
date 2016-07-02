
import unittest

def suite():
    suite = unittest.TestSuite()

    # Adding all tests
    from tests.schema.builders.mysql import MysqlSchemaBuilderTest
    suite.addTests(map(MysqlSchemaBuilderTest, ["testMysqlSchemaBuilder"]))

    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
