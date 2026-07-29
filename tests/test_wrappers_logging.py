def test_wrappers():

    from mrich import get_logger

    logger = get_logger(__name__)

    # large header banner
    logger.h1("Welcome to mrich")

    # Regular & rich text printing
    logger.print(
        "mrich offers a simple print wrapper which plays nicely with live rich elements"
    )
    logger.print("Emphasis can be placed with different mrich functions:")
    logger.bold("bold text")
    logger.italic("italic text")
    logger.underline("underlined text")
    logger.print(
        "rich markup is also [bold green]supported[reset] via square-bracket syntax"
    )

    # smaller header banner
    logger.h2("Event logging function")

    # Successes, errors, and warnings
    logger.success("Success statements are the most eye-catching to the user")
    logger.error("Error statements are also highlighted")
    logger.warning("As are warnings")

    # Other pre-made styles:
    logger.debug("Inobtrusive debug statements")
    logger.prompt("Eye-catching prompt")
    logger.reading("this_file_is_being_read.txt")
    logger.writing("this_file_is_being_written.txt")
    logger.disk("this_file_is_being_munged.txt", prefix="Modifying")

    # Format variables:
    number = 101
    numbers = [1, 2, 4, 51, 2]
    logger.var(number)
    logger.var(numbers)
    logger.var(len(numbers))
    logger.var("variable", "value")
    logger.var("#samples", 123)
    logger.var("frequency", 12.7, "GHz")
    logger.var("file", "/example/path/file.html")
    logger.var("green number", 456, separator=":", color="green")

    # smaller section separator/header
    logger.h3("This is a smaller header panel")

    # return

    # dynamic elements

    import time

    with logger.clock("Waiting for something"):
        time.sleep(1)

    with logger.loading("Loading"):
        time.sleep(1)
        logger.print("Interruptions don't disrupt live elements")
        time.sleep(2)

    with logger.spinner("Spinning"):
        time.sleep(1)

    for i in logger.track(range(20), prefix="tracking progress", total=20):
        time.sleep(0.2)
        if i == 9:
            logger.print("halfway there!")
            logger.var(i)
            logger.set_progress_field("i_halfway", i)

    # tabular data
    import pandas as pd

    df = pd.DataFrame(
        [
            dict(a=1, b=2),
            dict(a=2, b=3),
            dict(a=3, b=4),
            dict(a=4, b=5),
        ]
    )
    logger.print("This is a dataframe printed as a rich.Table", df)

    raise ValueError("rich formatted traceback is enabled by default")


if __name__ == "__main__":
    test_wrappers()
