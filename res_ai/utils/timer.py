from functools import wraps
from time import time


def time_this(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(
            "\nfile:%r | func:%r | took: %2.4f sec\n"
            % (f.__globals__["__file__"].split("/")[-1], f.__name__, te - ts)
        )
        return result

    return wrap
