# sourcery skip: avoid-builtin-shadow
import streamlit as st
from utils.form_utils import GenerateForm
from local.cache import *


global type,engine,gen
page = st.container()
type = None
engine = None
gen = None

col1, col2 = st.columns([1,1])
sqlalchemy_databases =tuple(database_engines.keys())

with col1:
    type = st.selectbox(
        "Select connection type",
        ("Python", "JDBC")
    )

with col2:
    engine = st.selectbox(
        "Select Database",
        sqlalchemy_databases
    )

if type == "Python":
   gen =  GenerateForm("python",engine=engine)
    
    
elif type =="JDBC":
    gen = GenerateForm("jdbc")