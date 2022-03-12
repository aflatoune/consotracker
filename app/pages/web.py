import streamlit as st


class Web:
    def __init__(self, **kwargs):
        self.kwargs = kwargs if isinstance(kwargs, dict) else {}
        self.title = self.kwargs.get('page_title', 'ConsoTracker')
        self.set_config()
        if self.kwargs.get('hide_tag', True):
            self.hide_tag()
        if self.kwargs.get('hide_dev_menu', False):
            self.hide_dev_menu()

    def set_config(self):
        st.set_page_config(page_title=self.title,
                           page_icon="chart_with_upwards_trend",
                           layout='wide',
                           initial_sidebar_state='expanded',
                           menu_items={"Get help": None,
                                       "Report a Bug": None,
                                       "About": None})
        st.header(self.title)

    def hide_tag(self):
        hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}
        #bui-2 > div > ul.st-d6.st-cp.st-as.st-at.st-by.st-bz.st-fw.st-fx.st-bc.st-bd.st-av.st-aw.st-ax.st-ay.st-fr.st-fy.st-fz.st-g0 > ul:nth-child(6) {display: none;}
        #bui-2 > div > ul.css-1uh038d.e1pxm3bq7 > ul {display: none;}
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    def hide_dev_menu(self):
        hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
        st.markdown(hide_menu_style, unsafe_allow_html=True)

    def v_spacer(self, height, sb=False) -> None:
        for _ in range(height):
            if sb:
                st.sidebar.write('\n')
            else:
                st.write('\n')

    def __str__(self):
        str(self.kwargs)
