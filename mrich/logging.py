import logging

from rich.logging import RichHandler
from rich.text import Text


class MrichHandler(RichHandler):
    """RichHandler that renders Rich renderables attached to log records directly."""

    def __init__(self, console=None, **kwargs):
        if console is None:
            from .console import console as mrich_console

            console = mrich_console
        kwargs.setdefault("show_time", False)
        kwargs.setdefault("show_level", False)
        kwargs.setdefault("show_path", False)
        super().__init__(console=console, **kwargs)

    def render_message(self, record, message):
        renderable = getattr(record, "_rich_renderable", None)
        if renderable is not None:
            return renderable
        return super().render_message(record, message)

    def emit(self, record):
        from .wrappers import CURRENT_PROGRESS, clear_progress

        if CURRENT_PROGRESS is not None:
            if CURRENT_PROGRESS.finished:
                clear_progress()
            else:
                message = self.format(record)
                message_renderable = self.render_message(record, message)
                log_renderable = self.render(
                    record=record, traceback=None, message_renderable=message_renderable
                )
                CURRENT_PROGRESS.console.print(log_renderable)
                return

        super().emit(record)


class PlainTextFormatter(logging.Formatter):
    """Formatter that strips Rich styling from renderables for plain-text handlers."""

    def format(self, record):
        renderable = getattr(record, "_rich_renderable", None)
        if renderable is not None:
            if hasattr(renderable, "plain"):
                record.msg = renderable.plain
            else:
                from io import StringIO
                from rich.console import Console

                buf = StringIO()
                Console(file=buf, no_color=True, highlight=False, width=120).print(
                    renderable
                )
                record.msg = buf.getvalue().rstrip("\n")
            record.args = None
        return super().format(record)


class MrichLogger:
    """Wraps a logging.Logger to expose the mrich function API as methods."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @property
    def name(self):
        return self._logger.name

    def _emit(self, level, renderable, plain_message=None):
        if not self._logger.isEnabledFor(level):
            return
        msg = plain_message or getattr(renderable, "plain", str(renderable))
        record = self._logger.makeRecord(
            self._logger.name, level, "(mrich)", 0, msg, (), None
        )
        record._rich_renderable = renderable
        self._logger.handle(record)

    def warning(self, *messages, **kwargs):
        from .functions import _build_warning

        self._emit(logging.WARNING, _build_warning(*messages, **kwargs))

    def debug(self, *messages, **kwargs):
        from .functions import _build_debug

        self._emit(logging.DEBUG, _build_debug(*messages, **kwargs))

    def error(self, *messages, **kwargs):
        from .functions import _build_error

        self._emit(logging.ERROR, _build_error(*messages, **kwargs))

    def success(self, *messages, **kwargs):
        from .functions import _build_success

        self._emit(logging.INFO, _build_success(*messages, **kwargs))

    def bold(self, *messages, **kwargs):
        from .functions import _build_bold

        self._emit(logging.INFO, _build_bold(*messages, **kwargs))

    def italic(self, *messages, **kwargs):
        from .functions import _build_italic

        self._emit(logging.INFO, _build_italic(*messages, **kwargs))

    def underline(self, *messages, **kwargs):
        from .functions import _build_underline

        self._emit(logging.INFO, _build_underline(*messages, **kwargs))

    def print(self, *args, **kwargs):
        from .wrappers import _build_print

        renderables = _build_print(*args)
        text = Text(" ".join(str(r) for r in renderables))
        self._emit(logging.INFO, text)

    def prompt(self, *messages, **kwargs):
        from .functions import _build_prompt

        self._emit(logging.INFO, _build_prompt(*messages, **kwargs))

    def reading(self, message):
        from .functions import _build_disk

        self._emit(logging.INFO, _build_disk(message, prefix="Reading"))

    def writing(self, message):
        from .functions import _build_disk

        self._emit(logging.INFO, _build_disk(message, prefix="Writing"))

    def disk(self, message, *, prefix):
        from .functions import _build_disk

        self._emit(logging.INFO, _build_disk(message, prefix=prefix))

    def h1(self, message):
        from .functions import _build_h1

        self._emit(logging.INFO, _build_h1(message))

    def h2(self, message):
        from .functions import _build_h2

        self._emit(logging.INFO, _build_h2(message))

    def h3(self, message):
        from .functions import _build_h3

        self._emit(logging.INFO, _build_h3(message))

    def header(self, *messages, **kwargs):
        self.bold(*messages, **kwargs)

    def var(self, *args, separator="=", color=None, highlight_if_rich_dunder=False):
        import inspect
        from .functions import _build_var

        frame = inspect.currentframe().f_back
        nargs = len(args)

        if nargs == 1:
            import re

            call_line = inspect.getframeinfo(frame).code_context[0].strip()
            match = re.search(r"\.var\((.+?)\)", call_line)

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
            variable, value = args
            unit = None
        elif nargs == 3:
            variable, value, unit = args
        else:
            raise ValueError("Wrong number of arguments to mrich.var()")

        objects, _ = _build_var(
            variable,
            value,
            unit,
            separator=separator,
            color=color,
            highlight_if_rich_dunder=highlight_if_rich_dunder,
        )
        text = Text()
        for i, obj in enumerate(objects):
            if i > 0:
                text.append(" ")
            if isinstance(obj, Text):
                text.append_text(obj)
            else:
                text.append(str(obj))

        self._emit(logging.DEBUG, text)

    def track(self, *args, **kwargs):
        from .wrappers import track

        return track(*args, **kwargs)

    def spinner(self, *args, **kwargs):
        from .spinners import spinner

        return spinner(*args, **kwargs)

    def loading(self, *args, **kwargs):
        from .spinners import loading

        return loading(*args, **kwargs)

    def clock(self, *args, **kwargs):
        from rich.text import Text
        from .spinners import clock

        def _on_complete(message):
            self._emit(logging.INFO, Text(message))

        return clock(*args, _on_complete=_on_complete, **kwargs)

    def set_progress_field(self, *args, **kwargs):
        from .wrappers import set_progress_field

        return set_progress_field(*args, **kwargs)

    def increment_progress_field(self, *args, **kwargs):
        from .wrappers import increment_progress_field

        return increment_progress_field(*args, **kwargs)


_loggers = {}


def _logger_has_effective_handler(logger):
    """Check whether a logger or any of its ancestors has a handler configured."""
    current = logger
    while current:
        if current.handlers:
            return True
        if not current.propagate:
            break
        current = current.parent
    return False


def get_logger(name: str) -> MrichLogger:
    """Get or create an MrichLogger for the given name.

    If the underlying logging.Logger has no effective handler, a MrichHandler
    is added automatically so output appears on the console by default.
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)

    if not _logger_has_effective_handler(logger):
        logger.addHandler(MrichHandler())
        logger.setLevel(logging.DEBUG)

    mrich_logger = MrichLogger(logger)
    _loggers[name] = mrich_logger
    return mrich_logger
