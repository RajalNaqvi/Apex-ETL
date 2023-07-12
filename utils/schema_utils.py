from shillelagh.backends.apsw.db import connect
from gsheetsdb import connect
import pandas as pd
import time


def get_datatypes_and_default_values(sheet_link):
    """
    Retrieves data types and default values from a Google Sheets document using SQL, then
    stores the result in a Pandas dataframe.

    :return: Pandas dataframe containing data types and default values
    """
    # Establish connection to database
    conn = connect()

    # Execute SQL query to retrieve data types and default values from Google Sheets
    result = conn.execute("""
        SELECT
            *
        FROM
            "{sheet_link}"
    """.format(sheet_link=sheet_link), headers=1)

    # Convert query result to Pandas dataframe
    df = pd.DataFrame(result.fetchall())

    # Return dataframe with data types and default values
    return df
