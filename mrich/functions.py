from .console import console, console_print
from rich.text import Text
from .colors import COLOR_LOOKUP
from .tools import strip_formats, restyle_arg
import inspect

### STYLES


def _build_bold(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text.strip())
    text.stylize("bold")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def bold(*messages, **kwargs):
    return console_print(_build_bold(*messages, **kwargs))


def _build_italic(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text.strip())
    text.stylize("italic")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def italic(*messages, **kwargs):
    return console_print(_build_italic(*messages, **kwargs))


def _build_underline(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text.strip())
    text.stylize("underline")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def underline(*messages, **kwargs):
    return console_print(_build_underline(*messages, **kwargs))


### LOG


def _build_warning(*messages, **kwargs):
    text = " Warning "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("warning")
    text.stylize("reverse bold", 0, 9)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def warning(*messages, **kwargs):
    return console_print(_build_warning(*messages, **kwargs))


def _build_error(*messages, **kwargs):
    text = " ERROR "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("error")
    text.stylize("reverse", 0, 7)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def error(*messages, **kwargs):
    return console_print(_build_error(*messages, **kwargs))


def _build_success(*messages, **kwargs):
    text = " Success "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("success")
    text.stylize("reverse", 0, 9)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def success(*messages, **kwargs):
    return console_print(_build_success(*messages, **kwargs))


def _build_debug(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text.strip())
    text.stylize("debug")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def debug(*messages, **kwargs):
    return console_print(_build_debug(*messages, **kwargs))


def _build_prompt(*messages, **kwargs):
    text = ">>>"
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}")
    text.stylize("bold purple")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return text


def prompt(*messages, **kwargs):
    return console_print(_build_prompt(*messages, **kwargs))


def _build_disk(message: str, *, prefix: str):
    message = str(message)
    text = Text(f" DISK  {prefix} {message}...")
    text.stylize("file", 0, 6)
    text.stylize("reverse bold", 0, 6)
    text.stylize("file", 8 + len(prefix), 8 + len(prefix) + len(message))
    return text


def disk(message: str, *, prefix: str):
    return console_print(_build_disk(message, prefix=prefix))


def reading(message):
    return disk(message, prefix="Reading")


def writing(message):
    return disk(message, prefix="Writing")


def _resolve_var_name_from_frame(frame, args):
    """Determines (variable, value, unit) from var()'s call-site, per its overload rules."""

    nargs = len(args)

    if nargs == 1:
        import re

        # get the variable name as defined in the code that called this function
        call_line = inspect.getframeinfo(frame).code_context[0].strip()
        match = re.search(r"var\((.+)\)", call_line)

        if match:
            variable = match.group(1).strip()
            func_match = re.match(r"len\((.+)\)$", variable)
            if func_match:
                variable = f"#{func_match.group(1).strip()}"
        else:
            variable = "arg"

        value = args[0]
        unit = None
    elif nargs == 2:
        variable = args[0]
        value = args[1]
        unit = None
    elif nargs == 3:
        variable = args[0]
        value = args[1]
        unit = args[2]
    else:
        raise ValueError("Wrong number of arguments to mrich.var()")

    return variable, value, unit


def _build_var(
    variable,
    value,
    unit=None,
    *,
    separator: str = "=",
    color: str | None = None,
    highlight_if_rich_dunder: bool = False,
):
    # style variable
    variable = Text(str(variable), style=COLOR_LOOKUP["var_name"])
    variable.stylize("bold")

    # to some type conversions if appropriate
    value = restyle_arg(value)

    if "Path" in str(type(value)):
        color = "file"

    if color and color in COLOR_LOOKUP:
        color = COLOR_LOOKUP[color]

    highlight = True
    if hasattr(value, "__rich__"):
        highlight = highlight_if_rich_dunder

    if color:
        value = Text(str(value), style=color)

    objects = [variable, separator, value]

    if unit:
        unit = Text(unit, style=COLOR_LOOKUP["var_type"])
        objects.append(unit)

    return objects, highlight


def var(
    *args,
    separator: str = "=",
    color: str | None = None,
    highlight_if_rich_dunder: bool = False,
):
    frame = inspect.currentframe().f_back
    variable, value, unit = _resolve_var_name_from_frame(frame, args)

    objects, highlight = _build_var(
        variable,
        value,
        unit,
        separator=separator,
        color=color,
        highlight_if_rich_dunder=highlight_if_rich_dunder,
    )

    console_print(*objects, markup=True, highlight=highlight)


### HEADINGS


def _build_h1(message):
    from rich.panel import Panel

    text = Text(message.upper(), justify="center")
    text.stylize("bold")
    return Panel(text)


def h1(message):
    return console.print(_build_h1(message))


def _build_h2(message):
    from rich.rule import Rule

    return Rule(message)


def h2(message):
    return console.rule(message)


def _build_h3(message):
    from rich.panel import Panel

    return Panel.fit(message)


def h3(message):
    return console.print(_build_h3(message))


### ALIASES


def header(*args, **kwargs):
    return bold(*args, **kwargs)
