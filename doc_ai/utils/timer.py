from functools import wraps
from time import time


def time_this(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func:%r took: %2.4f sec\n\n" % (f.__name__, te - ts))
        return result

    return wrap
