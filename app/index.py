import json
import logging as lg
import os
import streamlit as st
from pages.serie import Serie
from pages.web import Web

from consotracker.models import LinearRegression, PenalizedRegression, RandomForest
from consotracker.utils import match_dict

DICT_MODELS = {'LinearRegression': LinearRegression,
               'PenalizedRegression': PenalizedRegression,
               'RandomForest': RandomForest}

VERSION = os.environ.get('VERSION', 'v0.0.0')

if __name__ == '__main__':
    st_web = Web()
    st_serie = Serie()
    model_name = st.sidebar.selectbox(
        "Modèle", list(DICT_MODELS.keys()), index=0)

    with open("app/configs/gtrends.json") as f1, open ("app/configs/dbnomics.json") as f2:
        dict_kw = json.load(f1)
        dict_dbcodes = json.load(f2)

    sector_list = match_dict(dict_kw, dict_dbcodes)
    if "dict_dfs" not in st.session_state or "dict_series" not in st.session_state:
        dict_dfs, dict_series = st_serie.dl_data(dict_kw, dict_dbcodes)
        st.session_state["dict_dfs"] = dict_dfs
        st.session_state["dict_series"] = dict_series

    for sector in sector_list:
        st.subheader(f'{dict_dbcodes[sector]["label"]}')
        graph = st.empty()
        metrics = st.empty()
        st_web.v_spacer(height=0, sb=False)
        with st.spinner(text="Chargement"):
            graph.empty()
            fig, lm_model = st_serie.create_serie(
                dict(st.session_state["dict_dfs"]),
                dict(st.session_state["dict_series"]),
                DICT_MODELS[model_name], sector)
        predicted_df = lm_model.predicted_df
        predicted_df = predicted_df.round({"obs": 2, "pred": 2})
        st_serie.plot_alt2(predicted_df, graph)
        st_serie.add_metrics(predicted_df, metrics)
        st_web.v_spacer(height=3)
    # version
    st_web.v_spacer(height=10, sb=True)
    st.sidebar.caption(f"Version : {VERSION}")
