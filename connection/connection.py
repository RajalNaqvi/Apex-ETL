import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu

from utils.local_connection_utils import read_all_configs


Python = st.container()
Java = st.container()


configs = read_all_configs()
container_css = {
    "container": {"max-width": "25%", "margin": "0px !important"}}


with Python:
    Python.header("Python")
    python_names = []
    for config in configs['python']:
        python_names.append(config['connection_name'] if "connection_name" in config else None)
        
        
    selected2 = option_menu(None, python_names,
                            menu_icon="cast", default_index=0, orientation="horizontal", styles=container_css
                            )

with Java:
    Java.header("Java")
    java_names = []
    for config in configs['java']:
        java_names.append(config['connection_name'] if "connection_name" in config else None)
    selected2 = option_menu(None, java_names,
                            menu_icon="cast", default_index=0, orientation="horizontal",styles=container_css)
