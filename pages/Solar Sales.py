import streamlit as st
from PIL import Image
import sql
from functions import extract_snowflake_noload, convert_df
import pandas as pd
from datetime import date
import plotly.express as px
OBJECTIVE_Q1 = 2400
OBJECTIVE_YR = 18000
today = date.today()
today_formatted = today.strftime('%Y%m%d')
year, week_num, day_of_week = today.isocalendar()
st.sidebar.markdown("# Solar Sales")

image = Image.open('Holaluz_Logo_RGB_Gradient-.png')
image_ns = image.resize([int(0.11 * s) for s in image.size])

st.image(image_ns)

col1, col2 = st.columns(2)

col1.title('Solar Sales')
solar_sales_2023 = extract_snowflake_noload(sql.QUERY_SOLAR_SALES_2023).iloc[0]["solar_sales"]
col2.metric(f"Total {year}", f"{solar_sales_2023}")

st.sidebar.metric(f"Objective Q1", f"{'{:,}'.format(OBJECTIVE_Q1).replace(',', '.')}",
                  f"{'{:,}'.format(solar_sales_2023-OBJECTIVE_Q1).replace(',', '.')}")

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

solar_sales_last_15_days = extract_snowflake_noload(sql.QUERY_SOLAR_SALES_LAST15DAYS)
solar_sales_last_15_days.rename(columns={'solar_sales': 'Sales', 'sale_date': 'Date'}, inplace=True)

col1, col2 = st.columns(2)
col1.dataframe(solar_sales_last_15_days)

fig = px.line(solar_sales_last_15_days, x='Date', y='Sales', markers=True, color_discrete_sequence=['#F06B18'],
              width=600, height=400)
fig.update_yaxes(categoryorder="category ascending")
col2.plotly_chart(fig)

csv_solar_sales = convert_df(solar_sales_last_15_days)

st.download_button(
   "Download",
   csv_solar_sales,
   f"Solar_Sales_{today_formatted}.csv",
   "text/csv",
   key='download-csv'
)

st.markdown("""---""")
st.subheader('Last 15 days solar sales map')
solar_sales_map = extract_snowflake_noload(sql.QUERY_SOLAR_SALES_MAP)
solar_sales_map = solar_sales_map.dropna()
solar_sales_map[["lat", "lon"]] = solar_sales_map[["lat", "lon"]].apply(pd.to_numeric)
st.map(solar_sales_map)