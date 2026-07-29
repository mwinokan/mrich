import time
from contextlib import contextmanager

from .console import console


# spinners
def spinner(*args, **kwargs):
    if args:
        status = args[0]
        args = args[1:]
    else:
        status = "working..."
    return console.status(status, *args, spinner="line", **kwargs)


def loading(*args, **kwargs):
    if args:
        status = args[0]
        args = args[1:]
    else:
        status = "loading..."
    return console.status(status, *args, spinner="aesthetic", **kwargs)


@contextmanager
def clock(*args, _on_complete=None, **kwargs):
    if args:
        status = args[0]
    else:
        status = "waiting..."
    start = time.perf_counter()
    with console.status(status, spinner="clock", **kwargs):
        yield
    elapsed = time.perf_counter() - start
    message = f"{status} took {elapsed:.3f} seconds"
    if _on_complete:
        _on_complete(message)
    else:
        console.print(message)
