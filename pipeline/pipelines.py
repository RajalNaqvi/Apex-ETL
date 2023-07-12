import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from utils.generic_utils import set_page_config

from utils.local_connection_utils import read_all_pipeline_configs, read_pipeline_detals
from utils.form_utils import create_button_columns

from utils.style_utils import load_css

set_page_config(page_title="My Pipelines",page_icon=None,initial_sidebar_state="expanded",layout="wide",menu_items={})

load_css()

Pipelines = st.container()
Java = st.container()

configs = read_all_pipeline_configs()




if st.session_state.clicked_button in configs:
    st.session_state.selected_pipeline_pipeline_page = st.session_state.clicked_button
else:
    st.session_state.selected_pipeline_pipeline_page = configs[0]


#st.session_state.selected_pipeline_pipeline_page = st.session_state.clicked_button if st.session_state.clicked_button in configs else configs[0]

def kpi_generator(col,title,metric):
    with col:
        st.metric(title,metric)


side_col = st.columns(1)

col1, col2, col3, col4, col5, col6 = st.columns(6)

details = {}

with Pipelines:
    Pipelines.header("Pipelines")
    create_button_columns(configs)
    
col1, col2, col3, col4 = st.columns(4)
details = read_pipeline_detals(st.session_state.selected_pipeline_pipeline_page)["last_run"]

kpi_generator(col1, "Rows Read", details["rows_read"])
kpi_generator(col2, "Rows Write", details["rows_write"])
kpi_generator(col3, "Start Time", details["start_time"])
kpi_generator(col4, "End Time", details["end_time"])
    

    