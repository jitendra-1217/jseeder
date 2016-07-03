
# Notes:
# - While calling any seeder util/func/method, if it requires pass the self.ctx object
#   for it to use.
# - **Try cleaning ctx.cache after every table is processed

class DataGen():


    def __init__(self, ctx):
        self.ctx = ctx
        

    def generate(self, schemaForDatagen):
        pass
