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


def test_get_logger_prints_to_console_by_default():
    import mrich
    from mrich.logging import MrichHandler

    name = "mrich.test.default_handler"
    logging.getLogger(name).propagate = False  # isolate from pytest's root capture handler
    logger = mrich.get_logger(name)

    assert any(isinstance(h, MrichHandler) for h in logger._logger.handlers)
    assert logger._logger.isEnabledFor(logging.INFO)


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


def test_mrich_handler_routes_through_active_progress_console():
    import mrich
    from mrich import wrappers
    from mrich.logging import MrichHandler

    logger = logging.getLogger("mrich.test.handler_progress")
    logger.handlers.clear()
    logger.addHandler(MrichHandler())
    logger.setLevel(logging.DEBUG)

    mrich_logger = mrich.MrichLogger(logger)

    for i in mrich_logger.track(range(3)):
        progress_console = wrappers.CURRENT_PROGRESS.console
        calls = []
        original_print = progress_console.print
        progress_console.print = lambda *a, **k: calls.append((a, k)) or original_print(*a, **k)
        try:
            mrich_logger.warning("mid-progress message")
        finally:
            progress_console.print = original_print
        assert calls, "expected the record to print via the active progress console"
        break


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


def test_error_emits_error_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.error")
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.error("Something failed")

    assert len(records) == 1
    assert records[0].levelno == logging.ERROR
    assert "Something failed" in records[0]._rich_renderable.plain


def test_success_emits_info_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.success")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.success("It worked")

    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    assert "It worked" in records[0]._rich_renderable.plain


def test_bold_emits_info_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.bold")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.bold("bold text")

    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    assert "bold text" in records[0]._rich_renderable.plain


def test_italic_emits_info_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.italic")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.italic("italic text")

    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    assert "italic text" in records[0]._rich_renderable.plain


def test_underline_emits_info_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.underline")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.underline("underlined text")

    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    assert "underlined text" in records[0]._rich_renderable.plain


def test_print_emits_info_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.print")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.print("plain message")

    assert len(records) == 1
    assert records[0].levelno == logging.INFO


def test_prompt_emits_info_level_record():
    import mrich

    logger = mrich.get_logger("mrich.test.prompt")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.prompt("Eye-catching prompt")

    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    assert "Eye-catching prompt" in records[0]._rich_renderable.plain


def test_reading_and_writing_emit_info_level_records():
    import mrich

    logger = mrich.get_logger("mrich.test.diskio")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    logger.reading("input.txt")
    logger.writing("output.txt")

    assert len(records) == 2
    assert records[0].levelno == logging.INFO
    assert "input.txt" in records[0]._rich_renderable.plain
    assert "output.txt" in records[1]._rich_renderable.plain


def test_var_emits_debug_level_record_with_variable_name():
    import mrich

    logger = mrich.get_logger("mrich.test.var")
    logger._logger.setLevel(logging.DEBUG)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    number = 101
    logger.var(number)

    assert len(records) == 1
    assert records[0].levelno == logging.DEBUG
    assert "number" in records[0]._rich_renderable.plain
    assert "101" in records[0]._rich_renderable.plain


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


def test_clock_emits_completion_message_as_log_record():
    import mrich

    logger = mrich.get_logger("mrich.test.clock")
    logger._logger.setLevel(logging.INFO)
    records = []
    logger._logger.addHandler(_RecordCollector(records))

    with logger.clock("Waiting for something"):
        pass

    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    assert "Waiting for something" in records[0]._rich_renderable.plain
    assert "seconds" in records[0]._rich_renderable.plain

