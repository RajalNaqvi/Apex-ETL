import extra_streamlit_components as stx
import streamlit as st
from utils.local_connection_utils import read_all_configs, read_config
from utils.generic_utils import extract_connections_py_or_java, fetch_metadata
from utils.sqlalchemy_engine_utils import SQLAlchemyEngine


val = stx.stepper_bar(steps=["Select Source & Target", "Spark Settings", "Finish"])

if "source_type_index" not in st.session_state:
    st.session_state.source_type_index = 0
if "source_selected_index" not in st.session_state:
    st.session_state.source_selected_index = 0
if "source_selected_schema_index" not in st.session_state:
    st.session_state.source_selected_schema_index = 0
if "source_selected_table_index" not in st.session_state:
    st.session_state.source_selected_table_index = 0   

if "target_type_index" not in st.session_state:
    st.session_state.target_type_index = 0
if "target_selected_index" not in st.session_state:
    st.session_state.target_selected_index = 0
if "target_selected_schema_index" not in st.session_state:
    st.session_state.target_selected_schema_index = 0
if "target_selected_table_index" not in st.session_state:
    st.session_state.target_selected_table_index = 0   
    
source_type = "Python"
con_type = ["Python","Java"]

configs = read_all_configs()

if val == 0:
    source = ""
    source_div = st.expander("Source",expanded=True)
    with source_div:
        source_schema = ""
        source_tables = ""

        options = []
        subcol1, subcol2 = st.columns([3,1])
        with subcol2:
            source_type = st.radio("Source Type",con_type,index=st.session_state.source_type_index)
            st.session_state.source_type_index = con_type.index(source_type)
            options = extract_connections_py_or_java(source_type,configs)
        with subcol1:
            source = st.selectbox("Source",options=options,index=st.session_state.source_selected_index)
            st.session_state.source_selected_index = options.index(source) if source is not None else 0

        table_col, schema_col = st.columns([2,3])
        metadata = fetch_metadata(source)
        source_schema = metadata['schema']
        source_tables = metadata['tables']
        
        with table_col:
            source_int_schema = st.selectbox("Source Schema",source_schema,index=st.session_state.source_selected_schema_index)
            st.session_state.source_selected_schema_index = source_schema.index(source_int_schema)
        with schema_col:
            source_int_tables = st.selectbox("Source Table",source_tables[st.session_state.source_selected_schema_index],index=st.session_state.source_selected_table_index)
            st.session_state.source_selected_table_index = source_tables[st.session_state.source_selected_schema_index].index(source_int_tables)
        
    target_div = st.expander("Target")
    with target_div:
        target_schema = ""
        target_tables = ""

        options = []
        subcol1, subcol2 = st.columns([3,1])
        with subcol2:
            target_type = st.radio("Target Type",con_type,index=st.session_state.target_type_index)
            st.session_state.target_type_index = con_type.index(target_type)
            options = extract_connections_py_or_java(target_type,configs)
        with subcol1:
            target = st.selectbox("Target",options=options,index=st.session_state.target_selected_index)
            st.session_state.target_selected_index = options.index(target) if target is not None else 0

        table_col, schema_col = st.columns([2,3])
        metadata = fetch_metadata(target)
        target_schema = metadata['schema']
        target_tables = metadata['tables']
        
        with table_col:
            target_int_schema = st.selectbox("Target Schema",target_schema,index=st.session_state.target_selected_schema_index)
            st.session_state.target_selected_schema_index = target_schema.index(target_int_schema)
        with schema_col:
            target_int_tables = st.selectbox("Target Table",target_tables[st.session_state.target_selected_schema_index],index=st.session_state.target_selected_table_index)
            st.session_state.target_selected_table_index = target_tables[st.session_state.target_selected_schema_index].index(target_int_tables)

elif val ==1:
    st.write("hi")
