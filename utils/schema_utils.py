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
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = declarative_base()
        self.metadata = MetaData()
        
    def create_dynamic_table(self, table_name):
        class DynamicTable(self.Base):
            __tablename__ = table_name
            id = Column(Integer, primary_key=True)

        return DynamicTable

    def create_table(self, table_name, json_data):
        try:
            DynamicTable = self.create_dynamic_table(table_name)

            for key, value in json_data.items():
                data_type = DATA_TYPE_MAPPING.get(type(value), String(255))
                setattr(DynamicTable, key, Column(data_type))
                    
            self.Base.metadata.create_all(self.engine)
            
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
            data_type (object): The desired `python datatype` methods for the column, enum: (`str`, `float`, `bool`, `float`, `list`).

        Returns: 
        """
        try:
            self.metadata.reflect(bind=self.engine, only=[table_name])
            existing_table = self.metadata.tables[table_name]
            
            DynamicTable = self.create_dynamic_table(existing_table)
            
            mapped_data_type = self.DATA_TYPE_MAPPING.get(data_type, String(255))
            
            setattr(DynamicTable, column_name, Column(column_name, mapped_data_type))
            DynamicTable.__table__.create(bind=self.engine, checkfirst=True)
            
            return True, f"`{table_name}` column `{column_name}` datatype Altered"
        except Exception as e:
            return False, str(e)
        
    def drop_table(self, table_name):
        pass

    def commit_changes(self):
        self.session.commit()

    def close_session(self):
        self.session.close()
        
    def __exit__(self):
        self.session.close()