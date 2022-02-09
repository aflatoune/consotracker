import streamlit as st
from consotracker.models import LinearRegression, PenalizedRegression, RandomForest
from consotracker.preprocessing import Processing
from consotracker.utils import (download_dbseries, download_gtrends,
                                read_dbcode_from_csv, read_kw_from_csv,
                                mae, mda, rmse)
import altair as alt
import pandas as pd

alt.renderers.set_embed_options(actions=False)

class Serie:
    def __init__(self):
        pass

    def create_serie(self, model, choice):
        dict_kw = read_kw_from_csv("./gtrends_test.csv")
        dict_dbcodes = read_dbcode_from_csv("./series_test.csv")
        dict_dfs = download_gtrends(dict_kw)
        dict_series = download_dbseries(dict_dbcodes)

        X = dict_dfs[choice]
        y = dict_series[choice]
        processor = Processing()
        X = processor.fit(X)
        X_train = X.iloc[:216, :]
        X_test = X.iloc[217, :]

        lm_model = model()
        lm_model.fit(X_train, y)
        lm_model.predict(X_test)
        fig = lm_model.plot()
        return fig, lm_model

    def plot_alt(self, date, df, box):
        d_init, d_last = date
        mask_df = df[(df.date >= pd.to_datetime(d_init)) & (df.date <= pd.to_datetime(d_last))]
        melted_df = mask_df.melt('date', var_name='type', value_name='value')
        domain = [melted_df.value.min(), melted_df.value.max()]
        c = alt.Chart(melted_df).mark_line().encode(
            alt.X('date:T'),
            alt.Y('value:Q', scale=alt.Scale(domain=domain)),
            alt.Color('type:N')
        ).interactive()
        box.altair_chart(c, use_container_width=True)

    def add_metrics(self, date, df, box):
        d_init, d_last = date
        mask_df = df[(df.date >= pd.to_datetime(d_init)) & (df.date <= pd.to_datetime(d_last))]
        data_select = mask_df.dropna()
        _, col2, col3, col4, _ = box.columns(5)
        col2.metric("MAE", mae(obs=data_select.obs, pred=data_select.pred, round_value=3))
        col3.metric("RMSE", rmse(obs=data_select.obs, pred=data_select.pred, round_value=3))
        col4.metric("MDA", mda(obs=data_select.obs, pred=data_select.pred, round_value=3))


class SideBar:
    pass