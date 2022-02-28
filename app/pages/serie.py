import streamlit as st
import altair as alt
import pandas as pd

from dateutil.relativedelta import relativedelta
from consotracker.models import LinearRegression, PenalizedRegression, RandomForest
from consotracker.preprocessing import Processing
from consotracker.utils import (download_dbseries, download_gtrends,
                                match_dict, mae, mda, rmse)

alt.renderers.set_embed_options(actions=False)


class Serie:
    def __init__(self):
        pass

    def dl_data(self, dict_kw, dict_dbcodes):
        match_dict(dict_kw, dict_dbcodes)
        dict_dfs = download_gtrends(dict_kw)
        dict_series = download_dbseries(dict_dbcodes)
        return dict_dfs, dict_series

    def create_serie(self, dict_dfs, dict_series, model, choice):
        X = dict_dfs[choice]
        y = dict_series[choice]
        processor = Processing()
        X = processor.fit(X)

        sup_date = y.index.max()
        pred_date = sup_date + relativedelta(months=1)
        X_train = X[X.index <= sup_date]
        X_test = X.loc[sup_date]

        lm_model = model()
        lm_model.fit(X_train, y)
        lm_model.predict(X_test)
        fig = lm_model.plot()
        return fig, lm_model

    def plot_alt(self, date, df, box):
        d_init, d_last = date
        mask_df = df[(df.date >= pd.to_datetime(d_init)) &
                     (df.date <= pd.to_datetime(d_last))]
        melted_df = mask_df.melt('date', var_name='type', value_name='value')
        domain = [melted_df.value.min(), melted_df.value.max()]
        c = alt.Chart(melted_df).mark_line().encode(
            alt.X('date:T'),
            alt.Y('value:Q', scale=alt.Scale(domain=domain)),
            alt.Color('type:N')
        ).interactive()
        box.altair_chart(c, use_container_width=True)

    def plot_alt2(self, df, box):
        melted_df = df.melt('date', var_name='type', value_name='value')
        domain = [melted_df.value.min(), melted_df.value.max()]

        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['date'], empty='none')

        c = alt.Chart(melted_df).mark_line().encode(
            alt.X('yearmonth(date):T', title=""),
            alt.Y('value:Q', scale=alt.Scale(domain=domain), title=""),
            alt.Color('type:N')
        )

        selectors = alt.Chart(melted_df).mark_point().encode(
            x='yearmonth(date):T', opacity=alt.value(0),).add_selection(nearest)
        points = c.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
        text = c.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'value:Q', alt.value(' ')))
        rules = alt.Chart(melted_df).mark_rule(color='gray').encode(
            x='yearmonth(date):T',).transform_filter(nearest)
        layers = alt.layer(c, selectors, points, rules,
                           text).properties(width=600, height=300)
        box.altair_chart(layers, use_container_width=True)

    def add_metrics(self, df, box):
        data_select = df.dropna()
        metric1 = mae(obs=data_select.obs,
                      pred=data_select.pred, round_value=3)
        metric2 = rmse(obs=data_select.obs,
                       pred=data_select.pred, round_value=3)
        metric3 = mda(obs=data_select.obs,
                      pred=data_select.pred, round_value=3)
        st.write("MAE:", metric1, " RMSE: ", metric2, " MDA: ", metric3)


class SideBar:
    pass
