import streamlit as st
from .engine_utils import Engine
import pandas as pd
from .local_connection_utils import store_connection_config


class GenerateForm():

    def __init__(self, type, engine):
        if type == "python":
            self.python_form(engine=engine)

    def python_form(self, engine):  # sourcery skip: raise-specific-error

        host = None
        username = None
        password = None
        port = None
        database = None
        connection_name = None


        with st.form('python', clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                connection_name = st.text_input(
                    'Connection name',  placeholder="demo db connection")
                host = st.text_input(
                    'Hostname',  placeholder="db.example.com")
                username = st.text_input('username',  placeholder="John Doe")
                password = st.text_input(
                    'Password',  type="password", placeholder="Top secret password. No @")
            with col2:
                port = st.number_input('port', min_value=1)
                database = st.text_input(
                    'Database',  placeholder="testDB")

            if submit := st.form_submit_button(
                "Create connection"
            ):
                check = self.check_missing_values(connection_name=connection_name,
                                                    hostname=host, username=username, password=password, port=port, database=database, engine=engine)
                if check[0]:
                    st.error(f"{check[1]} is missing")
                else:
                    test_passed = Engine(connection_name=connection_name,
                                            hostname=host, username=username, password=password, port=port, database=database, engine=engine).test()

                    json_data = {"hostname": host, "username": username, "password": password,
                                    "port": port, "database": database, "engine": engine,"connection_type":"python"}
                    stored = store_connection_config(
                        filename=connection_name, json_data=json_data) if test_passed else False
                    if stored:
                        st.success('Connection created!', icon="✅")

    def create_connection(self, *args, **kwargs):
        print('args', args)
        print('kwargss', kwargs)
        print("Creating connection...")

    def check_missing_values(self, **kwargs):
        for key, value in kwargs.items():
            if len(str(value)) < 1:
                return True,  key
        return False, None


def create_button_columns(names):
    # Calculate the number of columns
    num_columns = 4
    # Calculate the total number of names
    num_names = len(names)
    # Calculate the number of rows required
    num_rows = (num_names + num_columns - 1) // num_columns

    # Iterate over each row
    for row in range(num_rows):
        # Create the desired number of columns
        cols = st.columns(num_columns)
        # Calculate the start and end index for names in the current row
        start_index = row * num_columns
        end_index = min(start_index + num_columns, num_names)
        
        # Iterate over the names in the current row
        for i in range(start_index, end_index):
            cols[i % num_columns].image("local/images/icon1.png")
            # Display the name as a button in the corresponding column
            cols[i % num_columns].button(names[i],use_container_width=True)