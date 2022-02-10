import streamlit as st
from pages.serie import Serie
from pages.web import Web

from consotracker.models import LinearRegression, PenalizedRegression, RandomForest

dict_models = {'LinearRegression': LinearRegression,
               'PenalizedRegression': PenalizedRegression,
               'RandomForest': RandomForest}


if __name__ == '__main__':
    st_web = Web()
    st_serie = Serie()
    serie = st.sidebar.selectbox("Série", ["FZ", "DE"], index=0)
    model_name = st.sidebar.selectbox("Modèle", list(dict_models.keys()), index=0)

    graph = st.empty()
    metrics = st.empty()
    l, c, r = st.columns(3)
    with c:
        st_web.v_spacer(height=5, sb=False)
        with st.spinner(text='Chargement'):
            graph.empty()
            metrics.empty()
            fig, lm_model = st_serie.create_serie(dict_models[model_name], serie)
    predicted_df = lm_model.predicted_df

    d = st.sidebar.date_input(
        "Filtre temporel",
        value=(predicted_df.date.min().date(),
               predicted_df.date.max().date()),
        min_value=predicted_df.date.min().date(),
        max_value=predicted_df.date.max().date())
    st_serie.plot_alt(d, predicted_df, graph)
    st_serie.add_metrics(d, predicted_df, metrics)
