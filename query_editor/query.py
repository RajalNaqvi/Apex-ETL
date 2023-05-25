import streamlit as st
from utils.local_connection_utils import read_all_configs, read_config
from utils.engine_utils import Engine
import pandas as pd
from sqlalchemy import text


configs = read_all_configs()

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


def fetch_metadata():
    try:
        metadata = read_config(connections)['data']
        del metadata['connection_type']
        metadata = Engine(**metadata).get_metadata()
        return metadata
    
    except Exception as e:
        return {"schema":[],"tables":[]}
    
def execute(query):
    try:
        metadata = read_config(connections)['data']
        del metadata['connection_type']
        return Engine(**metadata).execute_query(query)
    except Exception as e:
        return pd.DataFrame()
    

with query_tab:
    col1,col2 = query_tab.columns([5,2])

    with query_tab.container():
        with col1:
            py_or_java = st.radio("Choose type",["Python","Java"])
            if py_or_java =="Python":
                options.extend(config["connection_name"] for config in configs['python'])
            else:
                options.extend(config["connection_name"] for config in configs['java'])

            connections = st.selectbox("Select connection to use",options=options)
            query = st.text_area(label="Query editor",placeholder="Select * from mytable",height=300)
            metadata = fetch_metadata()
        if submit := st.button("Submit"):

            df = execute(query=query)
            st.session_state['query_df'] = df
            st.dataframe(df)

        with col2:
            st.write("Table Metadata")
            for data in metadata["schema"]:
                with st.expander(data):
                    lst = metadata["tables"][metadata["schema"].index(data)]
                    for i in lst:
                        st.markdown(i)
        
        
with graph_tab:
    choice = st.selectbox("Chart type",["Bar","Line","Area"])
    df = st.session_state['query_df']
    
    if choice == "Bar":
        st.bar_chart(df)
    elif choice == "Line":
        st.line_chart(df)
    elif choice == "Area":
        st.area_chart(df)

