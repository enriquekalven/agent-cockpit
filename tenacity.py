def retry(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

def wait_exponential(*args, **kwargs):
    return None

def stop_after_attempt(*args, **kwargs):
    return None
