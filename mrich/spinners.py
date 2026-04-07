from .console import console


# spinners
def spinner(*args, **kwargs):
    if args:
        status = args[0]
    else:
        status = "working..."
    return console.status(status, *args, spinner="line", **kwargs)


def loading(*args, **kwargs):
    if args:
        status = args[0]
    else:
        status = "loading..."
    return console.status(status, *args, spinner="aesthetic", **kwargs)


def clock(*args, **kwargs):
    if args:
        status = args[0]
    else:
        status = "waiting..."
    return console.status(status, *args, spinner="clock", **kwargs)
