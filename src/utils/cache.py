
cacheStore = {}

# --------------------
# Methods for cacheStore operations
def getCacheKey(key, default=None):
    return cacheStore.get(key, default)


def setCacheKey(key, val):
    cacheStore[key] = val


def emptyCache():
    cacheStore = {}

# --------------------
