from .sqlalchemy_engine_utils import SQLAlchemyEngine
from .local_connection_utils import read_config
import streamlit as st

"""This module contains utilitiy functions which can be used in particular case and are not relevant to any one scenario.
"""




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
    
def execute(connection,query):
    """Execute a query on the given connection

    Args:
        connection (string): Name of the connection 
        query (string): The query to execute

    Returns:
        Dataframe: Database response in dataframe
    """
    metadata = read_config(connection)['data']
    return SQLAlchemyEngine(**metadata).execute_query(query)