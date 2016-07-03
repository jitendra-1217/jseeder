
cacheStore = {}

# --------------------
# Methods for cacheStore operations
def getCacheKey(key):
    return cacheStore.get(key, None)


def setCacheKey(key, val):
    cacheStore[key] = val


def emptyCache():
    cacheStore = {}

# --------------------
