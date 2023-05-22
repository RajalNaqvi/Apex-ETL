import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu

Python, Java, CSharp = st.columns([1,1,1])


def new_page():
    switch_page("create_connection_form")



    # Now add a submit button to the form:



with Python:
    Python.header("Python")
    if postgres := st.button('Postgres'):
        switch_page("home")

with Java:
    Java.header("Java")
    st.button('2')
    selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    print(selected2)

with CSharp:
    CSharp.header("C#")
    st.button('3')
