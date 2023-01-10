import streamlit as st
from PIL import Image
import sql
from functions import extract_snowflake_noload, convert_df
from datetime import date
import plotly.express as px
OBJECTIVE_Q1 = 1400
today = date.today()
today_formatted = today.strftime('%Y%m%d')
year, week_num, day_of_week = today.isocalendar()
st.sidebar.markdown("# Solar Installations")

image = Image.open('Holaluz_Logo_RGB_Gradient-.png')
image_ns = image.resize([int(0.11 * s) for s in image.size])

st.image(image_ns)

col1, col2 = st.columns(2)

col1.title('Solar Installations')
solar_installations = extract_snowflake_noload(sql.QUERY_SOLAR_INSTALLATIONS_2023).iloc[0]["solar_installations"]
col2.metric(f"Total {year}", f"{solar_installations}")
st.sidebar.metric(f"Objective Q1", f"{'{:,}'.format(OBJECTIVE_Q1).replace(',', '.')}",
                  f"{'{:,}'.format(solar_installations-OBJECTIVE_Q1).replace(',', '.')}")
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

solar_installations_last_15_days = extract_snowflake_noload(sql.QUERY_SOLAR_INSTALLATIONS_LAST15)
solar_installations_last_15_days.rename(columns={'solar_installations': 'Installations', 'fecha': 'Date'}, inplace=True)

col1, col2 = st.columns(2)
col1.dataframe(solar_installations_last_15_days)

fig = px.line(solar_installations_last_15_days, x='Date', y='Installations', markers=True,
              color_discrete_sequence=['#F06B18'],
              width=600, height=400)
fig.update_yaxes(categoryorder="category ascending")
col2.plotly_chart(fig)

csv_solar_installations = convert_df(solar_installations_last_15_days)

st.download_button(
   "Download",
   csv_solar_installations,
   f"Solar_Installations_{today_formatted}.csv",
   "text/csv",
   key='download-csv'
)
