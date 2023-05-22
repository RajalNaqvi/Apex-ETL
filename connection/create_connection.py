# sourcery skip: avoid-builtin-shadow
import streamlit as st
from utils.form_utils import GenerateForm

page = st.container()
type = None

with page:
    type = st.selectbox(
        "Select connection type",
        ("Python", "JDBC", "ODBC")
    )
    
    if type == "Python":
        GenerateForm("python")
    elif type =="JDBC":
        GenerateForm("jdbc")