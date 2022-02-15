from pkgutil import get_data
import streamlit as st
from pages.serie import Serie
from pages.web import Web

from consotracker.models import LinearRegression, PenalizedRegression, RandomForest

DICT_MODELS = {'LinearRegression': LinearRegression,
               'PenalizedRegression': PenalizedRegression,
               'RandomForest': RandomForest}


if __name__ == '__main__':
    st_web = Web()
    st_serie = Serie()
    model_name = st.sidebar.selectbox(
        "Modèle", list(DICT_MODELS.keys()), index=0)
    dict_dfs, dict_series = st_serie.get_data()
    sector_list = dict_series.keys()

    cols = st.columns(len(sector_list))
    for col, sector in zip(cols, sector_list):
        with col:
            st.subheader(f'{sector}')
            graph = st.empty()
            metrics = st.empty()
            st_web.v_spacer(height=0, sb=False)
            with st.spinner(text="Chargement"):
                graph.empty()
                fig, lm_model = st_serie.create_serie(
                    dict_dfs, dict_series, DICT_MODELS[model_name], sector)
            predicted_df = lm_model.predicted_df
            predicted_df = predicted_df.round({"obs": 2, "pred": 2})
            st_serie.plot_alt2(predicted_df, graph)
            st_serie.add_metrics(predicted_df, metrics)
