# All contexts must extend this class

class AbstractContext():


    def __init__(self, conn, inputConfig):
        self.conn = conn
        self.inputConfig = inputConfig
