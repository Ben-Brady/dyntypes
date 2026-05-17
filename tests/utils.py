def test(name: str):
    def wrapper(func):
        func.__globals__[" " + name] = func

    return wrapper
