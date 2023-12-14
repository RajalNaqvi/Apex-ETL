import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from utils.generic_utils import set_page_config

from utils.local_connection_utils import read_connection_configs
from utils.form_utils import create_button_columns

from utils.style_utils import load_css

set_page_config(page_title="My Connections",page_icon=None,initial_sidebar_state="expanded",layout="wide",menu_items={})

load_css()

Python = st.container()
Java = st.container()


configs = read_connection_configs()
container_css = {
    "container": {"width": "25%", "margin": "0px !important","font-size": "14px","min-height": "30px", "white-space": "nowrap","overflow": "hidden","text-overflow": "ellipsis" }}


python_selected = None
java_selected = None

side_col = st.columns(1)

col1, col2, col3, col4, col5, col6 = st.columns(6)


with Python:
    Python.header("Python")
    python_names = [
        config['connection_name'] if "connection_name" in config else None
        for config in configs['python']
    ]
    create_button_columns(python_names)
        
    
    
with Java:
    Java.header("Java")
    java_names = [
        config['connection_name'] if "connection_name" in config else None
        for config in configs['java']
    ]
    create_button_columns(java_names)

