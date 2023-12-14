# sourcery skip: avoid-builtin-shadow
import streamlit as st
from utils.form_utils import GenerateForm
from local.cache import *
from utils.generic_utils import set_page_config
from utils.style_utils import load_css

set_page_config(page_title="Create Connections",page_icon=None,initial_sidebar_state="expanded",layout="wide",menu_items={})

load_css()


global type_, engine, gen
page = st.container()
type_ = None
engine = None
gen = None

col1, col2 = st.columns([1,1])
sqlalchemy_databases =tuple(sqlalchemy_database_engines.keys())

with col1:
    type_ = st.selectbox(
        "Select connection type",
        ("Python", "JDBC")
    )

with col2:
    engine = st.selectbox(
        "Select Database",
        sqlalchemy_databases
    )

if type_ == "Python":
   gen =  GenerateForm("python",engine=engine)
    
    
elif type_ =="JDBC":
    gen = GenerateForm("jdbc",engine=engine)