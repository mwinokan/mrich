def test_wrappers():

    import mrich

    # large header banner
    mrich.h1("Welcome to mrich")

    # Regular & rich text printing
    mrich.print(
        "mrich offers a simple print wrapper which plays nicely with live rich elements"
    )
    mrich.print("Emphasis can be placed with different mrich functions:")
    mrich.bold("bold text")
    mrich.italic("italic text")
    mrich.underline("underlined text")
    mrich.print(
        "rich markup is also [bold green]supported[reset] via square-bracket syntax"
    )

    # smaller header banner
    mrich.h2("Event logging function")

    # Successes, errors, and warnings
    mrich.success("Success statements are the most eye-catching to the user")
    mrich.error("Error statements are also highlighted")
    mrich.warning("As are warnings")

    # Other pre-made styles:
    mrich.debug("Inobtrusive debug statements")
    mrich.prompt("Eye-catching prompt")
    mrich.reading("this_file_is_being_read.txt")
    mrich.writing("this_file_is_being_written.txt")
    mrich.disk("this_file_is_being_munged.txt", prefix="Modifying")

    # Format variables:
    number = 101
    mrich.var(number)
    mrich.var("variable", "value")
    mrich.var("#samples", 123)
    mrich.var("frequency", 12.7, "GHz")
    mrich.var("file", "/example/path/file.html")
    mrich.var("green number", 456, separator=":", color="green")

    # smaller section separator/header
    mrich.h3("This is a smaller header panel")

    return

    # dynamic elements

    import time

    with mrich.clock("Waiting for something"):
        time.sleep(1)

    with mrich.loading("Loading"):
        time.sleep(1)
        mrich.print("Interruptions don't disrupt live elements")
        time.sleep(2)

    with mrich.spinner("Spinning"):
        time.sleep(1)

    for i in mrich.track(range(20), prefix="tracking progress", total=20):
        time.sleep(0.2)
        if i == 9:
            mrich.print("halfway there!")
            mrich.set_progress_field("i_halfway", i)

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
    mrich.print("This is a dataframe printed as a rich.Table", df)

    raise ValueError("rich formatted traceback is enabled by default")


if __name__ == "__main__":
    test_wrappers()
