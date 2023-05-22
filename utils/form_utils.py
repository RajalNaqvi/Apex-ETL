import streamlit as st


class GenerateForm():
    def __init__(self, type):
        if type == "python":
            self.python_form()

    def python_form(self):  # sourcery skip: raise-specific-error

        disabled = True

        col1, col2 = st.columns(2)

        host = None
        username = None
        password = None
        port = None
        database = None
        value = ""
        numeric_value = 5432

        with st.form('python', clear_on_submit=True):
            with col1:
                host = st.text_input(
                    'Hostname',  placeholder="db.example.com")
                username = st.text_input('username',  placeholder="John Doe")
                password = st.text_input(
                    'Password',  type="password", placeholder="Top secret password. No @")
            with col2:
                port = st.number_input('port',min_value=1)
                database = st.text_input(
                    'Database',  placeholder="testDB")

            if submit := st.form_submit_button(
                "Create connection", type='primary'
            ):
                if port.isalnum():
                    check = self.check_missing_values(
                        hostname=host, username=username, password=password, port=port, database=database)
                    if check[0]:
                        st.error(f"{check[1]} is missing")
                

    def create_connection(self, *args, **kwargs):
        print('args', args)
        print('kwargss', kwargs)
        print("Creating connection...")

    def check_missing_values(self, **kwargs):  # sourcery skip: remove-dict-items
        print(kwargs, 'line50 here')
        for key, value in kwargs.items():
            if len(value) < 1:
                return True,  key
        return False, None
