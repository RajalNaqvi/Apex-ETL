import streamlit as st
from local.cache import *
import sqlalchemy as sq


class Engine():

    def __init__(self, engine, hostname, username, password, port, database, connection_name):
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
