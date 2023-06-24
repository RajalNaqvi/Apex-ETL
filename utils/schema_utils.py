from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ARRAY
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
            return True
        except Exception as e:
            return False

    def alter_table(self, table_name, alteration):
        pass

    def drop_table(self, table_name):
        pass

    def commit_changes(self):
        self.session.commit()

    def close_session(self):
        self.session.close()
        
    def __exit__(self):
        self.session.close()