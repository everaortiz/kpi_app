import pandas as pd
import streamlit as st
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine


@st.experimental_memo(ttl=600)
def extract_snowflake_noload(query):
    url = URL(**st.secrets["snowflake"])
    engine = create_engine(url)
    connection = engine.connect()
    df = pd.read_sql(query, connection)
    return df

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

"""@st.experimental_memo(ttl=600)
def extract_snowflake_noload(query):
    conn = init_connection()
    cur = conn.cursor()
    cur.execute(query)
    while True:
        dat = cur.fetchmany(50000)
        if not dat:
            break
        df = pd.DataFrame(dat, columns=cur.description)
    return df"""


"""@st.cache(allow_output_mutation=True)
def extract_snowflake_noload(sql):
    conn = init_connection()
    print('Conexion realizada')
    cur = conn.cursor().execute(sql)
    df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
    return df"""

# @st.cache(allow_output_mutation=True)
"""def extract_snowflake_noload(sql):
    # Extract from Snowflake
    conn = init_connection()


    sf_client = SnowflakeSQLClient(**st.secrets["snowflake"])
    df = []
    for chunk in sf_client.make_query(sql, chunksize=160000):
        df.append(chunk)
    df_tot = pd.concat(df, ignore_index=True)
    sf_client.close_connection()
    return df_tot"""


@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
