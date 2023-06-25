from importlib import metadata
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATA_TYPE_MAPPING = {
    str: String(255),
    bool: Boolean,
    int: Integer,
    float: Float,
    list: String(255)
}

class SchemaUtils:
    is_session_close = True
    def __init__(self, connection_string: str):
        """
        Initialize the SchemaUtils object.

        Args:
            connection_string (str): The connection string for the database.
        """
        self._engine = create_engine(connection_string)    
        
    def _create_session(self):
        """
        Create a new session and initialize metadata and base.
        """
        Session = sessionmaker(bind=self._engine)
        self.session = Session()
        self.Base = declarative_base()
        self.metadata = MetaData()
        
        self.is_session_close = False
        return True
        
    def create_dynamic_table(self, table_name: str):
        """
        Create a dynamic table class with the provided table name.

        Args:
            table_name (str): The name of the table.

        Returns:
            class: The dynamically created table class.
        """
        class DynamicTable(self.Base):
            __tablename__ = table_name
            id = Column(Integer, primary_key=True)

        return DynamicTable

    def create_table(self, table_name: str, json_data: dict):
        """
        Create a new table based on the provided table name and JSON data.

        Args:
            table_name (str): The name of the table.
            json_data (dict): The JSON data containing column names and values.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            DynamicTable = self.create_dynamic_table(table_name)

            for key, value in json_data.items():
                data_type = DATA_TYPE_MAPPING.get(type(value), String(255))
                setattr(DynamicTable, key, Column(data_type))
                    
            self.Base.metadata.create_all(self._engine)
            
            print(f"Table '{table_name}' created.")
            return True, f"Table '{table_name}' created."
        except Exception as e:
            return False, str(e)

    def alter_table(self, table_name: str, column_name: str, data_type: object):
        """
        Alter the specified column in the database table.

        Args:
            table_name (str): The name of the table.
            column_name (str): The name of the column to be altered.
            data_type (object): The desired Python data type for the column. Valid values are `str`, `float`, `bool`, `int`, `list`.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            self.metadata.reflect(bind=self._engine, only=[table_name])
            existing_table = self.metadata.tables[table_name]
            
            DynamicTable = self.create_dynamic_table(existing_table)
            
            mapped_data_type = DATA_TYPE_MAPPING.get(data_type, String(255))
            
            setattr(DynamicTable, column_name, Column(column_name, mapped_data_type))
            DynamicTable.__table__.create(bind=self._engine, checkfirst=True)
            
            return True, f"`{table_name}` column `{column_name}` datatype Altered"
        except Exception as e:
            return False, str(e)
        
    def drop_table(self, table_name: str):
        """
        Drop the specified table from the database.

        Args:
            table_name (str): The name of the table to drop.
        """
        pass

    def commit_changes(self):
        """
        Commit the changes made within the session.
        """
        self.session.commit()

    def close_session(self):
        """
        Close the session and set the session close flag.
        """
        self.session.close()
        self.is_session_close = True
        
    # Auto create and destroy session - if `with` context used
    def __enter__(self):
        """
        Enter the `with` context and create a new session.
        """
        self._create_session()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the `with` context and commit changes, close the session.
        """
        self.commit_changes()
        self.close_session()
     
# if __name__ == '__main__':
#     connection_creds = {
#         "username": "appx",
#         "password": "appx",
#         "host": "localhost",
#         "port": "3306",
#         "database": "mysql"
#     }
#     database_name = 'MySQL'
#     from local.cache import database_engines
#     database_connection = database_engines[database_name]
#     connection_string = f"{database_connection}://{connection_creds['username']}:{connection_creds['password']}@{connection_creds['host']}:{connection_creds['port']}/{connection_creds['database']}"
#     print(connection_string)
#     json_data = {
#         "name": "John Doe",
#         "age": 25,
#         "email": "johndoe@example.com",
#         "is_active": True,
#         "languages": ["Python", "JavaScript", "Java"]
#     }

#     utils = SchemaUtils(connection_string)

#     # Create a new table
#     table_name = 'user_table_new'
#     # utils.create_table(table_name, json_data)
#     print(utils.alter_table(table_name, "email", str))
#     utils.close_session()