
# Refs:
# (1) https://github.com/joke2k/faker
# (2) http://fake-factory.readthedocs.io/en/latest/providers/faker.providers.address.html

from faker import Factory
fake = Factory.create()


class Seeder():

    seedersMap = {
        "fake.name":           fake.name,
        "fake.street_address": fake.street_address,
        "fake.address":        fake.address,
        "fake.text":           fake.text,
        "fake.random_int":     fake.random_int,

        # More from fake-factor library can follow..
    }


    def __init__(self):
        # (1) Adds custom seeders funcs from module J
        from src.seeders.j import J
        j = J()
        self.seedersMap.update({
            "j.fromList":    j.fromList,
            "j.fromBetween": j.fromBetween
        })


    def callSeederFunc(self, fName, fArgsList={}):
        if fName in self.seedersMap:
            return self.seedersMap[fName](**fArgsList) if isinstance(fArgsList, dict) else self.seedersMap[fName](*fArgsList)

        raise Exception("Seeder func: {} - Not found".format(fName))


    def setUpMySQLSeeders(self, conn):
        from src.seeders.mysql import MySQL
        mysql = MySQL(conn)
        self.seedersMap.update({
            "mysql.seedFromTableRef": mysql.seedFromTableRef
        })
