from rich.table import Table


def df_to_table(df):

    import pandas as pd

    table = Table()

    if isinstance(df.index, pd.MultiIndex):
        multi = True
        for name in df.index.names:
            table.add_column(name)
    else:
        multi = False
        if df.index.name:
            table.add_column(df.index.name)
        else:
            table.add_column("index")

    for col in df.columns:
        table.add_column(str(col))

    for index, row in df.iterrows():

        values = []

        if multi:
            for name in index:
                values.append(str(name))
        else:
            values.append(str(index))

        for col in df.columns:
            values.append(str(row[col]))
        table.add_row(*values)

    return table


def array_to_table(a):
    from numpy import array
    from rich import box
    from rich.panel import Panel

    a = array(a)

    assert a.ndim == 2

    table = Table(show_header=False, show_lines=False, box=None, show_edge=True)

    for col in a.T:
        table.add_column()

    for row in a:
        values = []
        for value in row:
            values.append(str(value))
        table.add_row(*values)

    panel = Panel(table, expand=False)

    return panel
