from .console import console, console_print

dict_keys = type(dict().keys())


# wrappers
def print(*args, **kwargs):

    new_args = []

    for i, arg in enumerate(args):

        try:
            from pandas import DataFrame, Index

            if isinstance(arg, DataFrame):
                from .df import df_to_table

                # console_print(arg, type(arg))
                table = df_to_table(arg)
                new_args.append(table)
                continue

            elif isinstance(arg, Index):
                new_args.append(set(arg))
                continue

        except ModuleNotFoundError as e:
            pass
        except Exception as e:
            raise

        if isinstance(arg, dict_keys):
            new_args.append(set(arg))

        else:
            new_args.append(arg)

    console_print(*new_args, **kwargs)


def out(*args, **kwargs):
    console.out(*args, **kwargs)


def rule(*args, **kwargs):
    console.rule(*args, **kwargs)


### PROGRESS

CURRENT_PROGRESS = None


def clear_progress():
    global CURRENT_PROGRESS
    CURRENT_PROGRESS = None


def track(*args, prefix: str = "Working...", **kwargs):

    from .colors import THEME
    from rich.console import Console
    from rich.progress import (
        Progress,
        TextColumn,
        BarColumn,
        TaskProgressColumn,
        TimeRemainingColumn,
        TimeElapsedColumn,
    )

    global CURRENT_PROGRESS

    console = Console(theme=THEME)

    CURRENT_PROGRESS = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields}"),
        # TextColumn("{task.fields[suffix]}"),
        console=console,
    )

    # CURRENT_PROGRESS.tasks[0].fields["suffix"] = ""

    with CURRENT_PROGRESS:
        yield from CURRENT_PROGRESS.track(*args, description=prefix, **kwargs)


def set_progress_field(key: str = None, value=None, **kwargs):
    progress = CURRENT_PROGRESS

    if not progress:
        return

    task = progress.tasks[0]

    if kwargs:
        for key, value in kwargs.items():
            task.fields[key] = value
    else:
        task.fields[key] = value


def set_progress_prefix(text):
    progress = CURRENT_PROGRESS

    if not progress:
        return

    task = progress.tasks[0]
    task.description = text


# def set_progress_suffix(text):
#     set_progress_field("suffix", text)
# task = progress.tasks[0]
# task.description = text
