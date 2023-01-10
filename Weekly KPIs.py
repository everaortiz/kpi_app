import streamlit as st
from PIL import Image
import sql
from functions import extract_snowflake_noload, convert_df
from datetime import date

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="expanded",
                   menu_items=None)

COLUMNS = ['Week', 'Date', 'Portfolio', 'Solar Sales', 'Solar Installations', 'Cloud Sales']

st.sidebar.markdown("# Weekly KPIs")

image = Image.open('Holaluz_Logo_RGB_Gradient-.png')
image_ns = image.resize([int(0.11 * s) for s in image.size])

st.image(image_ns)

today = date.today()
today_formatted = today.strftime('%Y%m%d')
year, week_num, day_of_week = today.isocalendar()

portfolio = extract_snowflake_noload(sql.QUERY_PORTFOLIO)
solar_sales = extract_snowflake_noload(sql.QUERY_SOLAR_SALES)
solar_installations = extract_snowflake_noload(sql.QUERY_SOLAR_INSTALLATIONS)
cloud_sales = extract_snowflake_noload(sql.QUERY_CLOUD_SALES)

df_merg_1 = portfolio.merge(solar_sales, on='week', how='left')
df_merg_2 = df_merg_1.merge(solar_installations, on='week', how='left')
df_total = df_merg_2.merge(cloud_sales, on='week', how='left')

df_total.rename(columns={'portfolio': 'Portfolio', 'solar_installations': 'Solar Installations',
                         'solar_sales': 'Solar Sales', 'cloud_sales': 'Cloud Sales', 'week': 'Week',
                         'fecha': 'Date'}, inplace=True)
df_total = df_total[COLUMNS]
df_total_filled = df_total.fillna(0)
df_total_filled['Cloud Sales'] = df_total_filled['Cloud Sales'].astype('int')

st.title('Weekly KPIs')

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(df_total_filled)
csv = convert_df(df_total_filled)


st.download_button(
   "Download",
   csv,
   f"KPIs_{today_formatted}.csv",
   "text/csv",
   key='download-csv')


st.subheader(f'W{week_num} vs W{week_num-1}')
st.caption('Current week vs last week')
last_week = df_total_filled[df_total_filled['Week'] == week_num-1]
current_week = df_total_filled[df_total_filled['Week'] == week_num]
lw_portfolio = last_week.iloc[0]["Portfolio"]
lw_solar_sales = last_week.iloc[0]["Solar Sales"]
lw_solar_installations = last_week.iloc[0]["Solar Installations"]
lw_cloud_sales = last_week.iloc[0]["Cloud Sales"]

cw_portfolio = current_week.iloc[0]["Portfolio"]
cw_solar_sales = current_week.iloc[0]["Solar Sales"]
cw_solar_installations = current_week.iloc[0]["Solar Installations"]
cw_cloud_sales = current_week.iloc[0]["Cloud Sales"]

col1, col2, col3, col4 = st.columns(4)

portfolio_formatted = "{:,}".format(cw_portfolio).replace(',', '.')

col1.metric("Portfolio", f"{portfolio_formatted}", f"{cw_portfolio - lw_portfolio}")
col2.metric("Solar Sales", f"{cw_solar_sales}", f"{cw_solar_sales - lw_solar_sales}")
col3.metric("Solar Installations", f"{cw_solar_installations}", f"{cw_solar_installations -lw_solar_installations}")
col4.metric("Solar Installations", f"{cw_cloud_sales}", f"{cw_cloud_sales - lw_cloud_sales}")

