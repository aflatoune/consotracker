import streamlit as st
from pages.serie import Serie
from pages.web import Web


if __name__ == '__main__':
    st_web = Web()
    st_serie = Serie()
    serie = st.sidebar.selectbox("Série", ["FZ", "DE"], index=0)
    with st.spinner(text='Training'):
        fig, lm_model = st_serie.create_serie(serie)
    predicted_df = lm_model.predicted_df

    d = st.sidebar.date_input("Filtre temporel",
                              value=(predicted_df.date.min().date(), predicted_df.date.max().date()),
                              min_value=predicted_df.date.min().date(),
                              max_value=predicted_df.date.max().date())
    st_serie.plot_alt(d, predicted_df)
    st_serie.add_metrics(d, predicted_df, 'obs', 'pred')