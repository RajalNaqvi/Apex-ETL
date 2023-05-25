import streamlit as st
from utils.local_connection_utils import read_all_configs, read_config
from utils.engine_utils import Engine
import pandas as pd
from sqlalchemy import text


configs = read_all_configs()

global options
options = []

col1,col2 = st.columns([5,2])
query_editor = st.container()
connections = ""

global metadata

metadata = {"schema":[],"tables":[]}
query = ""

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
        df =  Engine(**metadata).execute_query(query)
        return df
    except Exception as e:
        return pd.DataFrame()
    
    
with query_editor:
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
        st.dataframe(df)

    with col2:
        st.write("Table Metadata")
        for data in metadata["schema"]:
            with st.expander(data):
                lst = metadata["tables"][metadata["schema"].index(data)]
                for i in lst:
                    st.markdown(i)
    
    

