import streamlit as st
from consotracker.models import LinearRegression
from consotracker.preprocessing import Processing
from consotracker.metrics import MAE, RMSE
from consotracker.utils import (download_dbseries, download_gtrends,
                                read_dbcode_from_csv, read_kw_from_csv)
import altair as alt
import pandas as pd

alt.renderers.set_embed_options(actions=False)

class Serie:
    def __init__(self):
        pass

    def create_serie(self, choice):
        dict_kw = read_kw_from_csv("./gtrends_test.csv")
        dict_dbcodes = read_dbcode_from_csv("./series_test.csv")
        dict_dfs = download_gtrends(dict_kw)
        dict_series = download_dbseries(dict_dbcodes)

        X = dict_dfs[choice]
        y = dict_series[choice]["original_value"]
        y = y[-217:]
        processor = Processing()
        X = processor.fit(X)
        X_train = X.iloc[:-1, :]
        X_test = X.iloc[-1, :]

        lm_model = LinearRegression()
        lm_model.fit(X_train, y)
        lm_model.predict(X_test)
        fig = lm_model.plot()
        return fig, lm_model

    def plot_alt(self, date, df):
        d_init, d_last = date
        mask_df = df[(df.date >= pd.to_datetime(d_init)) & (df.date <= pd.to_datetime(d_last))]
        melted_df = mask_df.melt('date', var_name='type', value_name='value')
        domain = [melted_df.value.min(), melted_df.value.max()]
        c = alt.Chart(melted_df).mark_line().encode(
            alt.X('date:T'),
            alt.Y('value:Q', scale=alt.Scale(domain=domain)),
            alt.Color('type:N')
        ).interactive()
        st.altair_chart(c, use_container_width=True)

    def add_metrics(self, date, df):
        d_init, d_last = date
        mask_df = df[(df.date >= pd.to_datetime(d_init)) & (df.date <= pd.to_datetime(d_last))]
        data_select = mask_df.dropna()
        _, col2, col3, col4, _ = st.columns(5)
        col2.metric("MAE", MAE(data_select, 'obs', 'pred'))
        col3.metric("MSE", MAE(data_select, 'obs', 'pred'))
        col4.metric("MDA", 'X')


class SideBar:
    pass