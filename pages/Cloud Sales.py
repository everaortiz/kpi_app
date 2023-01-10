import streamlit as st
from PIL import Image
import sql
from functions import extract_snowflake_noload, convert_df
from datetime import date
import plotly.express as px
import pandas as pd

today = date.today()
today_formatted = today.strftime('%Y%m%d')
year, week_num, day_of_week = today.isocalendar()

st.sidebar.markdown("# Cloud Sales")

image = Image.open('Holaluz_Logo_RGB_Gradient-.png')
image_ns = image.resize([int(0.11 * s) for s in image.size])

st.image(image_ns)

col1, col2 = st.columns(2)

col1.title('Cloud Sales')
cloud_sales = extract_snowflake_noload(sql.QUERY_CLOUD_SALES_2023).iloc[0]["cloud_sales"]
col2.metric(f"Total {year}", f"{cloud_sales}")

st.markdown("""---""")
st.subheader('Last 15 days')

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

cloud_sales_last_15_days = extract_snowflake_noload(sql.QUERY_CLOUD_SALES_LAST15)
cloud_sales_last_15_days.rename(columns={'cloud_sales': 'Sales', 'fecha': 'Date'}, inplace=True)

col1, col2 = st.columns(2)
col1.dataframe(cloud_sales_last_15_days)

fig = px.line(cloud_sales_last_15_days, x='Date', y='Sales', markers=True,
              color_discrete_sequence=['#F06B18'],
              width=600, height=400)
fig.update_yaxes(categoryorder="category ascending")
col2.plotly_chart(fig)

csv_cloud_sales = convert_df(cloud_sales_last_15_days)

st.download_button(
   "Download",
   csv_cloud_sales,
   f"Cloud_Sales_{today_formatted}.csv",
   "text/csv",
   key='download-csv'
)

st.markdown("""---""")
st.subheader('Last 15 days cloud sales map')
cloud_sales_map = extract_snowflake_noload(sql.QUERY_CLOUD_SALES_MAP)
cloud_sales_map = cloud_sales_map.dropna()
cloud_sales_map[["lat", "lon"]] = cloud_sales_map[["lat", "lon"]].apply(pd.to_numeric)
st.map(cloud_sales_map)
