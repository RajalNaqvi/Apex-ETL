import streamlit as st
from local.cache import *
import sqlalchemy as sq
import pandas as pd
from sqlalchemy import text
from .style_utils import load_css

# IMPORTS FOR JDBAPI
import jaydebeapi
import zipfile
import requests
import sys

load_css()



class Engine():

    def __init__(self, engine, hostname, username, password, port, database, connection_name=None):
        engine = database_engines[engine]
        url = f"{engine}://{username}:{password}@{hostname}:{port}/{database}"

        self.conn = sq.create_engine(
            url=url
        )

    def test(self):
        try:
            self.conn.connect()
            return True
        except Exception as e:
            st.error(str(e))
            return False

    def get_metadata(self):
        inspector = sq.inspect(self.conn)
        schemas = inspector.get_schema_names()
        tables = []

        for schema in schemas:
            print(f"schema: {schema}")
            tables.append(inspector.get_table_names(schema=schema))
        return {"tables": tables,"schema": schemas}
    
    def execute_query(self,query):
        con = self.conn.connect()
        data = con.execute(text(query))
        df = pd.DataFrame(data)
        
        return df


class JDBCEngine():
    
    sys.path.append('../')

    def __init__(self,engine, hostname, username, password, port,database=None):
        
        with open("jar_maven_metada.json", "r") as maven_metada_file:
            maven_metada_file = maven_metada_file.loads()
        maven_details = maven_metada_file[engine]
        
        self.download_jar_from_maven(**maven_details,destination_path="./local/jars")
        jar_lib_path = f"./local/jars/{maven_details['artifact_id']}-{maven_details['version']}.jar"
        driver_classname = self.fetch_driver_classpath(jar_lib_path)
        engine = database_engines_jdbc[engine]
        
        connection_string = f"jdbc:{engine}://{username}:{password}@{hostname}:{port}/"
        if database:
            connection_string = connection_string+database
              
        self.conn = jaydebeapi.connect(driver_classname,connection_string,
                           [username,password],
                           jar_lib_path)

    def download_jar_from_maven(self,group_id, artifact_id, version, destination_path):
        # Maven Repository URL
        try:
            url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.jar"

            # Send a GET request to the Maven Repository URL
            response = requests.get(url)

            # Save the response content to a file
            with open(destination_path, 'wb') as file:
                file.write(response.content)

            print("JAR file downloaded successfully.")
        except Exception as e:
            print("Unable to Download JAR file from Maven Repository : EXCEPTION ::",e)
            
    def fetch_driver_classpath(self,jar_file_path):
        with zipfile.ZipFile(jar_file_path) as jar_file:
            manifest = jar_file.read("META-INF/services/java.sql.Driver").decode("utf-8")
        main_class = None
        for line in manifest.splitlines():
            main_class = line

        if main_class:
            return main_class
        else:
            return None

    def get_metadata(self):
        
        schemas = []
        schema_tables_metadata = {}
        
        resultSet = self.conn.jconn.getMetadData().getSchemas()
        cur  = self.conn.cursor()
        cur._rs = resultSet
        cur._meta = resultSet.getMetadata()
        result_list = cur.fetchall()
        
        # Appending schema names inside schemas list 
        [schemas.append(str(schema[0])) for schema in result_list if schema[0] not in schemas]
        
        # fetching tables metadata inisde each schema
        for schema in schemas:
            tables = []
            resultSet = self.conn.jconn.getMetaData.getTables(
                None,schema,"%",None
            )
            cur = self.conn.cursor()
            cur._rs = resultSet
            cur._meta = resultSet.getMetaData()
            result_list  = cur.fetchall()
            
            [tables.append(str(table[2])) for table in result_list if table[0] not in tables]
            
            schema_tables_metadata.update({
                schema:tables
            })
            
        return schema_tables_metadata

    def execute_query(self,query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            if cursor.rowcount > 0:
                # generating DataFrame Based on Column names
                dataset = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return pd.DataFrame(dataset,columns=columns)
            else:
                True
                
        except Exception as e:
            print(e)
            return False

class JDBCEngine():
    
    sys.path.append('../')

    def __init__(self,engine, hostname, username, password, port,database=None):
        
        with open("jar_maven_metada.json", "r") as maven_metada_file:
            maven_metada_file = maven_metada_file.loads()
        maven_details = maven_metada_file[engine]
        
        self.download_jar_from_maven(**maven_details,destination_path="./local/jars")
        jar_lib_path = f"./local/jars/{maven_details['artifact_id']}-{maven_details['version']}.jar"
        driver_classname = self.fetch_driver_classpath(jar_lib_path)
        engine = database_engines_jdbc[engine]
        
        connection_string = f"jdbc:{engine}://{username}:{password}@{hostname}:{port}/"
        if database:
            connection_string = connection_string+database
              
        self.conn = jaydebeapi.connect(driver_classname,connection_string,
                           [username,password],
                           jar_lib_path)

    def download_jar_from_maven(self,group_id, artifact_id, version, destination_path):
        # Maven Repository URL
        try:
            url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.jar"

            # Send a GET request to the Maven Repository URL
            response = requests.get(url)

            # Save the response content to a file
            with open(destination_path, 'wb') as file:
                file.write(response.content)

            print("JAR file downloaded successfully.")
        except Exception as e:
            print("Unable to Download JAR file from Maven Repository : EXCEPTION ::",e)
            
    def fetch_driver_classpath(self,jar_file_path):
        with zipfile.ZipFile(jar_file_path) as jar_file:
            manifest = jar_file.read("META-INF/services/java.sql.Driver").decode("utf-8")
        main_class = None
        for line in manifest.splitlines():
            main_class = line

        if main_class:
            return main_class
        else:
            return None

    def get_metadata(self):
        
        schemas = []
        schema_tables_metadata = {}
        
        resultSet = self.conn.jconn.getMetadData().getSchemas()
        cur  = self.conn.cursor()
        cur._rs = resultSet
        cur._meta = resultSet.getMetadata()
        result_list = cur.fetchall()
        
        # Appending schema names inside schemas list 
        [schemas.append(str(schema[0])) for schema in result_list if schema[0] not in schemas]
        
        # fetching tables metadata inisde each schema
        for schema in schemas:
            tables = []
            resultSet = self.conn.jconn.getMetaData.getTables(
                None,schema,"%",None
            )
            cur = self.conn.cursor()
            cur._rs = resultSet
            cur._meta = resultSet.getMetaData()
            result_list  = cur.fetchall()
            
            [tables.append(str(table[2])) for table in result_list if table[0] not in tables]
            
            schema_tables_metadata.update({
                schema:tables
            })
            
        return schema_tables_metadata

    def execute_query(self,query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            if cursor.rowcount > 0:
                # generating DataFrame Based on Column names
                dataset = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return pd.DataFrame(dataset,columns=columns)
            else:
                True
                
        except Exception as e:
            print(e)
            return False
