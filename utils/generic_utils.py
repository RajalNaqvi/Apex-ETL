from .sqlalchemy_engine_utils import SQLAlchemyEngine
from .local_connection_utils import read_config
import streamlit as st
from .jdbc_engine_utils import JDBCEngine

"""This module contains utilitiy functions which can be used in particular case and are not relevant to any one scenario.
"""

def set_page_config(page_title="AppX",menu_items={},initial_sidebar_state="expanded",page_icon=None,layout="wide"):
    st.set_page_config(page_title=page_title, page_icon=page_icon,initial_sidebar_state=initial_sidebar_state, layout=layout, menu_items=menu_items)


def extract_connections_py_or_java(py_or_java,configs):
    """Get connections from config variable and divide them into a list of python/java based connections.

    Args:
        py_or_java (string): Python or Java. The connections type to be fetched from config variable.
        configs (list): list of configurations

    Returns:
        _type_: list
    """
    options = []
    if py_or_java =="Python":
        options.extend(config["connection_name"] for config in configs['python'])
    else:
        options.extend(config["connection_name"] for config in configs['java'])
    return options

def fetch_metadata(connection):
    """Fetch metadata from the given connection.

    Args:
        connections (string): name of the connection 

    Returns:
        dict: {"tables": [],"schema":[]}
    """
    try:
        metadata = read_config(connection)['data']
        metadata = SQLAlchemyEngine(**metadata).get_metadata()
        return metadata
    except Exception as e:
        st.error(str(e))
        return {"tables": [],"schema":[]}
    
def execute(connection,query,is_java=False):
    """Execute a query on the given connection

    Args:
        connection (string): Name of the connection 
        query (string): The query to execute

    Returns:
        Dataframe: Database response in dataframe
    """
    metadata = read_config(connection)['data']
    
    if is_java:
        return JDBCEngine(**metadata).execute_query(query)
    return SQLAlchemyEngine(**metadata).execute_query(query)


def check_missing_values(**kwargs):
    """Check on submit connection if any form field is missing values.

    Returns:
        tuple: Boolean value indicating whether a key is missing value and the key. For e.g if hostname is null, True, hostname. Else False,None
    """
    for key, value in kwargs.items():
        if len(str(value)) < 1:
            return True,  key
    return False, None