def auto_complete_values(x):
    cols = x.columns.tolist()
    i = 0
    while i in range(0, len(cols)):
        x[cols[i]] = x[cols[i]].ffill().fillna(8).astype(int)
        i += 1
    return x


def auto_complete(x):
    cols = x.columns.tolist()
    i = 0
    while i in range(0, len(cols)):
        x[cols[i]] = x[cols[i]].ffill().fillna(0)
        i += 1
    return x


def name_columns(x):
    cols = x.columns.tolist()
    i = 1
    value = [cols[i]]
    name = ''.join(map(str, value))
    return name
