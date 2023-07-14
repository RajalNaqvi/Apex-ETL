import streamlit as st
from utils.local_connection_utils import read_connection_configs, read_config
from utils.sqlalchemy_engine_utils import SQLAlchemyEngine
from utils.generic_utils import extract_connections_py_or_java, fetch_metadata, execute, set_page_config
import pandas as pd
from sqlalchemy import text
from utils.style_utils import load_css
from pandas_profiling import ProfileReport
from datetime import datetime


set_page_config(page_title="Query Editor",page_icon=None,initial_sidebar_state="expanded",layout="wide",menu_items={})

configs = read_connection_configs()
load_css()
global options
options = []



connections = ""

global metadata
global df

metadata = {"schema":[],"tables":[]}
query = ""


if 'query_df' not in st.session_state:
    st.session_state['query_df'] = pd.DataFrame() 


query_tab, graph_tab = st.tabs(["Query", "Graph"])

    
df = None
with query_tab:
    col1,col2 = query_tab.columns([4,2])

    with query_tab.container():
        with col1:
            py_or_java = st.radio("Choose type",["Python","Java"])
            options = extract_connections_py_or_java(py_or_java,configs)
            
            connections = st.selectbox("Select connection to use",options=options)
            query = st.text_area(label="Query editor",placeholder="Select * from mytable",height=150)
            metadata = fetch_metadata(connections)
            if submit := st.button("Submit"):

                df = execute(connection=connections,query=query)
                st.session_state['query_df'] = df
                st.dataframe(df)

        with col2:
            st.write("Table Metadata")
            for data in metadata["schema"]:
                html_list = "<ul style=\"overflow:hidden;font-size:6px\">\n"
                with st.expander(data):
                    lst = metadata["tables"][metadata["schema"].index(data)]
                    for item in lst:
                        html_list += f" <li style=\"font-size:15px\">{item}</li>\n" 
                    html_list += "</ul>" 
                    st.markdown(html_list,unsafe_allow_html=True)

        
with graph_tab:
    if st.button("Download profile report"):
        df = st.session_state['query_df']
        profile = ProfileReport(df,progress_bar=True)
        profile.to_file(f'.local/profile_reports/{datetime.now()}.html')
    choice = st.selectbox("Chart type",["Bar","Line","Area"])
    df = st.session_state['query_df']
    
    if choice == "Bar":
        st.bar_chart(df)
    elif choice == "Line":
        st.line_chart(df)
    elif choice == "Area":
        st.area_chart(df)


