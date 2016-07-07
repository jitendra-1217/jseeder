# All schema builder must extend this class

class AbstractSchemaBuilder():


    def __init__(self, ctx):
        self.ctx = ctx


    def getCtx(self):
        return self.ctx


    # Get schema to be used by data generator
    def getSchemaForDataGen(self):
        raise NotImplementedError


    # Handles specific cases for few seeders
    def fixSeederArgs(self, tSchema, t):

        for f, fSchema in tSchema.items():

            # (1) Adding key - "table__field" as last argument for seeder to keep track of serial returns
            #    per table's field seed call
            if fSchema["seeder"] in ["j.fromList", "j.fromBetween"]:
                fSchema["seederArgs"].append("{}__{}".format(t, f))
