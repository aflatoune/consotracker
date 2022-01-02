from statsmodels.tsa.seasonal import STL


def _deseasonalize(df, mode):
    if mode == "stl":
        stl = STL(df, seasonal=13)
        res = stl.fit()
        return res.trend

    if mode == "yoy":
        return df.diff(12)


def _growth_wrt_date(df, date="2004-01-01"):
    base = df.loc[date][0]
    df = df.iloc[:,0].map(lambda x: (x/base - 1)*100)
    return df