import streamlit as st
from consotracker.models import LinearRegression
from consotracker.preprocessing import Processing
from consotracker.utils import (download_dbseries, download_gtrends,
                                read_dbcode_from_csv, read_kw_from_csv)
import altair as alt
import datetime
import pandas as pd

alt.renderers.set_embed_options(actions=False)


def create_serie():
    dict_kw = read_kw_from_csv("./gtrends_test.csv")
    dict_dbcodes = read_dbcode_from_csv("./series_test.csv")
    dict_dfs = download_gtrends(dict_kw)
    dict_series = download_dbseries(dict_dbcodes)

    X = dict_dfs["FZ"]
    y = dict_series["FZ"]["original_value"]
    y = y[-217:]
    processor = Processing()
    X = processor.fit(X)
    X_train = X.iloc[:-1, :]
    X_test = X.iloc[-1, :]

    lm_model = LinearRegression()
    lm_model.fit(X_train, y)
    lm_model.predict(X_test)
    fig, ax = lm_model.plot()
    return fig, lm_model


class Web:
    def __init__(self, kwargs=None):
        self.kwargs = kwargs

    def set_config(self):
        st.set_page_config(page_title='Consotracker',
                           page_icon=None,
                           layout='wide',
                           initial_sidebar_state='collapsed',
                           menu_items={"Get help": None,
                                       "Report a Bug": None,
                                       "About": None})
        st.header('Consotracker')

    def hide_tag(self):
        hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}

        #bui-2 > div > ul.st-d6.st-cp.st-as.st-at.st-by.st-bz.st-fw.st-fx.st-bc.st-bd.st-av.st-aw.st-ax.st-ay.st-fr.st-fy.st-fz.st-g0 > ul:nth-child(6) {display: none;}
        #bui-2 > div > ul.css-1uh038d.e1pxm3bq7 > ul {display: none;}
        </style>
        """

        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    def __str__(self):
        str(self.kwargs)


def plot_alt(d):
    mask_df = predicted_df[predicted_df.date >= pd.to_datetime(d)]
    melted_df = mask_df.melt('date', var_name='type', value_name='value')
    domain = [melted_df.value.min(), melted_df.value.max()]
    c = alt.Chart(melted_df).mark_line().encode(
        alt.X('date:T'),
        alt.Y('value:Q', scale=alt.Scale(domain=domain)),
        alt.Color('type:N')
    ).interactive()
    st.altair_chart(c, use_container_width=True)


def add_metrics(mae, mse, mda):
    _, col2, col3, col4, _ = st.columns(5)
    col2.metric("MAE", mae)
    col3.metric("MSE", mse)
    col4.metric("MDA", mda)


if __name__ == '__main__':
    st_web = Web()
    st_web.set_config()
    st_web.hide_tag()
    fig, lm_model = create_serie()
    predicted_df = lm_model.predicted_df

    d = st.sidebar.date_input("Date de début",
                              value=predicted_df.date.min().date(),
                              min_value=predicted_df.date.min().date(),
                              max_value=predicted_df.date.max().date())
    plot_alt(d)
    add_metrics(10, 20, 1)
