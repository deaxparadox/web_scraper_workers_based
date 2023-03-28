import time 

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start
        print(f"{func.__name__} => {total_time}")
        return result
    return wrapper

