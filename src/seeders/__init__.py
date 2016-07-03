
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
        "fake.name":    fake.name,
        "fake.address": fake.address,
        "fake.text":    fake.text,
        # More from fake-factor library can follow..
    }


    def __init__(self):
        pass


    def callSeederFunc(self, fName, fArgsList=[]):

        if fName in self.seedersMap:
            return self.seedersMap[fName](*fArgsList)

        raise Exception("Seeder func: {} - Not found".format(fName))


    def setUpMySQLSeeders(self):

        from src.seeders.mysql import MySQL
        mysql = MySQL()
        self.seedersMap.update({
            "mysql.seedFromTableRef": mysql.seedFromTableRef
        })
