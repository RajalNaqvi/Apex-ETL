import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu

from utils.local_connection_utils import read_all_pipeline_configs
from utils.form_utils import create_button_columns

from utils.style_utils import load_css
load_css()

Pipelines = st.container()
Java = st.container()


configs = read_all_pipeline_configs()
container_css = {
    "container": {"width": "25%", "margin": "0px !important","font-size": "14px","min-height": "30px", "white-space": "nowrap","overflow": "hidden","text-overflow": "ellipsis" }}


side_col = st.columns(1)

col1, col2, col3, col4, col5, col6 = st.columns(6)

details = {}

with Pipelines:
    Pipelines.header("Pipelines")
    create_button_columns(configs)
        
dashboard = st.expander("Dasher")
with dashboard:
    st.button("Dashboard")
    