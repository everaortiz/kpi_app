import streamlit as st
from holaluz_datatools import SnowflakeSQLClient
import pandas as pd


@st.cache(allow_output_mutation=True)
def extract_snowflake_noload(sql):
    """
    Execute a query in snowflake DB
    :param sql: code to execute
    :return: df with the result
    """
    # Extract from Snowflake
    sf_client = SnowflakeSQLClient(**st.secrets["snowflake"])
    df = []
    for chunk in sf_client.make_query(sql, chunksize=160000):
        df.append(chunk)
    df_tot = pd.concat(df, ignore_index=True)
    sf_client.close_connection()
    return df_tot


@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
