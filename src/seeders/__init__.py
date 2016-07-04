
# Notes:
# - All seeders are expected to be class with class methods
# - Few seedres'method may take first argument as ctx

# - Import all commited/deafult/new/temp seeders module here
# - Also, map all the methods/functions in use to the seedersMap variable

# fake-factory lib @ https://github.com/joke2k/faker
from faker import Factory
fake = Factory.create()


class Seeder():

    seedersMap = {
        # Add a mapping for fake module here, if using
        # Ref: http://fake-factory.readthedocs.io/en/latest/providers/faker.providers.address.html
        "fake.name":    fake.name,

        "fake.street_address": fake.street_address,
        "fake.address": fake.address,

        "fake.text":    fake.text,

        "fake.random_int": fake.random_int,
        # More from fake-factor library can follow..
    }


    def __init__(self):
        from src.seeders.j import J
        j = J()
        self.seedersMap.update({
            "j.fromList":    j.fromList,
            "j.fromBetween": j.fromBetween
        })


    def callSeederFunc(self, fName, fArgsList=[]):

        if fName in self.seedersMap:
            return self.seedersMap[fName](*fArgsList)

        raise Exception("Seeder func: {} - Not found".format(fName))


    def setUpMySQLSeeders(self, conn):

        from src.seeders.mysql import MySQL
        mysql = MySQL(conn)
        self.seedersMap.update({
            "mysql.seedFromTableRef": mysql.seedFromTableRef
        })
