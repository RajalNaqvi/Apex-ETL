from .sqlalchemy_engine_utils import SQLAlchemyEngine
from .local_connection_utils import read_config

def extract_connections_py_or_java(py_or_java,configs):
    options = []
    if py_or_java =="Python":
        options.extend(config["connection_name"] for config in configs['python'])
    else:
        options.extend(config["connection_name"] for config in configs['java'])
    return options

def fetch_metadata(connections):
    metadata = read_config(connections)['data']
    metadata = SQLAlchemyEngine(**metadata).get_metadata()
    return metadata
    
def execute(connections,query):
    metadata = read_config(connections)['data']
    return SQLAlchemyEngine(**metadata).execute_query(query)