import logging

from rich.logging import RichHandler


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

    def track(self, *args, **kwargs):
        from .wrappers import track

        return track(*args, **kwargs)


_loggers = {}


def get_logger(name: str) -> MrichLogger:
    """Get or create an MrichLogger for the given name."""
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    mrich_logger = MrichLogger(logger)
    _loggers[name] = mrich_logger
    return mrich_logger
