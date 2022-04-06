import os
import logging as lg
import streamlit as st
from distutils.util import strtobool
from consotracker.utils import Download
from pages import Serie
from pages import Web

from consotracker.redis import Redis
from consotracker.models import LinearRegression, PenalizedRegression, RandomForest

DICT_MODELS = {'LinearRegression': LinearRegression,
               'PenalizedRegression': PenalizedRegression,
               'RandomForest': RandomForest}

VERSION = os.environ.get('VERSION', 'v0.0.0')
STREAMLIT_DEV = strtobool(os.environ.get('STREAMLIT_DEV', 'true'))
PATH_CONFIG = os.path.join('app', 'configs')
CONTAINER_NAME = os.environ.get('CONTAINER_NAME', 'consotracker_bdd')

if __name__ == '__main__':
    st_web = Web(hide_dev_menu=STREAMLIT_DEV)
    st_serie = Serie()
    model_name = st.sidebar.selectbox(
        "Modèle", list(DICT_MODELS.keys()), index=0)

    db = Redis(host=CONTAINER_NAME, port=6379, db=0)
    dw = Download(PATH_CONFIG, db=db.api)

    sector_list = dw.match_dict(dw.dict_kw, dw.dict_dbcodes)
    if "dict_dfs" not in st.session_state or "dict_series" not in st.session_state:
        dict_dfs, dict_series = dw.dl_data()
        st.session_state["dict_dfs"] = dict_dfs
        st.session_state["dict_series"] = dict_series

    for sector in sector_list:
        st.subheader(f'{dw.dict_dbcodes[sector]["label"]}')
        graph = st.empty()
        metrics = st.columns(3)
        st_web.v_spacer(height=0, sb=False)
        with st.spinner(text="Chargement"):
            graph.empty()
            fig, lm_model = st_serie.create_serie(
                dict(st.session_state["dict_dfs"]),
                dict(st.session_state["dict_series"]),
                DICT_MODELS[model_name], sector)
        predicted_df = lm_model.predicted_df
        predicted_df = predicted_df.round({"obs": 2, "pred": 2})
        st_serie.plot_alt_v2(predicted_df, graph)
        st_serie.add_metrics(predicted_df, metrics)
        st_web.v_spacer(height=3)

    # version
    st_web.v_spacer(height=30, sb=True)
    st.sidebar.caption(f"Version : {VERSION}")