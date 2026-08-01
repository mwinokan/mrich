import re

dict_keys = type(dict().keys())


def detect_format_prefix(message):

    match = re.match(r"^\[.*?\]", message)

    if match:
        match = match.group()

    return match


def strip_formats(*messages, text="", separator=" "):
    formats = []
    start = len(text) + 1
    for message in messages:

        if hasattr(message, "__rich__"):
            message = message.__rich__()
        else:
            message = str(message)

        prefix = detect_format_prefix(message)

        prefix_found = prefix is not None

        if prefix_found:
            message = message.removeprefix(prefix)
            prefix = prefix.removeprefix("[").removesuffix("]")

        end = start + len(message)
        text += separator + message

        if prefix_found:
            formats.append((prefix, start, end + 2))

        start = end

    return text, formats


def restyle_arg(arg):

    ### PANDAS

    try:
        from pandas import DataFrame, Index

        if isinstance(arg, DataFrame):
            from .table import df_to_table

            # console_print(arg, type(arg))
            table = df_to_table(arg)
            return table

        elif isinstance(arg, Index):
            return set(arg)

    except ModuleNotFoundError:
        pass

    ### ARRAYS

    try:
        from numpy import array

        a = array(arg)

        match a.ndim:
            case 1:
                return list(arg)
            case 2:
                from .table import array_to_table

                return array_to_table(a)
            case _:
                pass

    except ModuleNotFoundError:
        pass

    ### SETS

    if isinstance(arg, dict_keys):
        return set(arg)

    else:
        return arg
