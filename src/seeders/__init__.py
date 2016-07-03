
# Notes:
# - All seeders are expected to be class with class methods
# - Few seedres'method may take first argument as ctx

# - Import all commited/deafult/new/temp seeders module here
# - Also, map all the methods/functions in use to the seedersMap variable

# fake-factory lib @ https://github.com/joke2k/faker
from faker import Factory
fake = Factory.create()

# Import other modules



seedersMap = {
    "fake.name":    fake.name,
    "fake.address": fake.address,
    "fake.text":    fake.text
    # More from fake-factor library can follow..


    # Functions from other modules can follow here..
}


# Util to call seeder funcs
def callSeederFunc(fName, fArgsList=[]):

    if fName in seedersMap:
        return seedersMap[fName](*fArgsList)

    raise Exception("Seeder func: {} - Not found".format(fName))
