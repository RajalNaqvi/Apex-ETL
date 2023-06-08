if "target_type_index" not in st.session_state:
    st.session_state.target_type_index = 0
if "target_selected_index" not in st.session_state:
    st.session_state.target_selected_index = 0
if "target_selected_schema_index" not in st.session_state:
    st.session_state.target_selected_schema_index = 0
if "target_selected_table_index" not in st.session_state:
    st.session_state.target_selected_table_index = 0   






if val == 0:
    target = ""
    target_div = st.expander("target",expanded=True)
    with target_div:
        target_schema = ""
        target_tables = ""

        options = []
        subcol1, subcol2 = st.columns([3,1])
        with subcol2:
            target_type = st.radio("target Type",con_type,index=st.session_state.target_type_index)
            st.session_state.target_type_index = con_type.index(target_type)
            options = extract_connections_py_or_java(target_type,configs)
        with subcol1:
            target = st.selectbox("target",options=options,index=st.session_state.target_selected_index)
            st.session_state.target_selected_index = options.index(target) if target is not None else 0

        table_col, schema_col = st.columns([2,3])
        metadata = fetch_metadata(target)
        target_schema = metadata['schema']
        target_tables = metadata['tables']
        
        with table_col:
            target_int_schema = st.selectbox("Schema",target_schema,index=st.session_state.target_selected_schema_index)
            st.session_state.target_selected_schema_index = target_schema.index(target_int_schema)
        with schema_col:
            target_int_tables = st.selectbox("Table",target_tables[st.session_state.target_selected_schema_index],index=st.session_state.target_selected_table_index)
            st.session_state.target_selected_table_index = target_tables[st.session_state.target_selected_schema_index].index(target_int_tables)
        