
import random

from src.utils import cache


class J():

    def __init__(self):
        pass


    def fromList(self, l, inSerial=True, k=""):
        if not inSerial:
            return random.choice(l)
        # Returns l elements in serial on every call "per" k
        k += "J__fromList"
        i = cache.getCacheKey(k, 0)
        cache.setCacheKey(k, i + 1)
        lLen = len(l)

        return l[i%lLen]


    def fromBetween(self, i, j, inSerial=True, k=""):
        return self.fromList(range(i, j + 1), inSerial, k)
