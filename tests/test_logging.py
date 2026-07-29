import logging


class _RecordCollector(logging.Handler):
    def __init__(self, records):
        super().__init__()
        self.records = records

    def emit(self, record):
        self.records.append(record)


def test_get_logger_returns_same_instance_for_same_name():
    import mrich

    logger_a = mrich.get_logger("mrich.test.identity")
    logger_b = mrich.get_logger("mrich.test.identity")

    assert logger_a is logger_b


def test_warning_emits_record_with_rich_renderable():
    import mrich

    logger = mrich.get_logger("mrich.test.warning")
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.warning("Something broke")

    assert len(records) == 1
    assert records[0].levelno == logging.WARNING
    assert hasattr(records[0], "_rich_renderable")
    assert "Something broke" in records[0]._rich_renderable.plain


def test_mrich_handler_renders_styled_output_to_console():
    from io import StringIO
    from rich.console import Console
    import mrich
    from mrich.logging import MrichHandler

    buf = StringIO()
    test_console = Console(file=buf, force_terminal=True, width=80)

    logger = logging.getLogger("mrich.test.handler")
    logger.handlers.clear()
    logger.addHandler(MrichHandler(console=test_console))
    logger.setLevel(logging.DEBUG)

    mrich_logger = mrich.MrichLogger(logger)
    mrich_logger.warning("Handler rendered this")

    output = buf.getvalue()
    assert "Handler rendered this" in output


def test_plain_text_formatter_strips_rich_markup():
    import mrich
    from mrich.logging import PlainTextFormatter

    logger = logging.getLogger("mrich.test.plaintext")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    formatted = []

    class _CapturingHandler(logging.Handler):
        def emit(self, record):
            formatted.append(self.format(record))

    handler = _CapturingHandler()
    handler.setFormatter(PlainTextFormatter("%(message)s"))
    logger.addHandler(handler)

    mrich_logger = mrich.MrichLogger(logger)
    mrich_logger.warning("Plain text please")

    assert len(formatted) == 1
    assert "Plain text please" in formatted[0]
    assert "\x1b[" not in formatted[0]


def test_debug_suppressed_when_level_above_debug():
    import mrich

    logger = logging.getLogger("mrich.test.levelfilter")
    logger.handlers.clear()
    logger.setLevel(logging.WARNING)

    records = []
    logger.addHandler(_RecordCollector(records))

    mrich_logger = mrich.MrichLogger(logger)
    mrich_logger.debug("Should not appear")

    assert records == []


def test_track_produces_no_log_records():
    import mrich

    logger = logging.getLogger("mrich.test.track")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    records = []
    logger.addHandler(_RecordCollector(records))

    mrich_logger = mrich.MrichLogger(logger)
    result = None
    for i in mrich_logger.track(range(10)):
        result = i

    assert result == 9
    assert records == []

