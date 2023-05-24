import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
from utils.local_connection_utils import create_con_directory


def __init__(file_name):
    st.set_page_config(page_title="AppX", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
    create_con_directory()

__init__("css/style.css")




show_pages(
    [
        Page("main.py", "Home"),
        Page("connection/create_connection.py","Create a new connection"),
        Page("connection/connection.py", "Connections")
    ]
)