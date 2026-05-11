def test(name: str):
    def wrapper(func):
        # automatically mark async tests
        # if inspect.iscoroutinefunction(func):
        #     func = pytest.mark.asyncio(func)

        func.__globals__[" " + name] = func

    return wrapper
