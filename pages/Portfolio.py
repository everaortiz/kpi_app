import streamlit as st
from PIL import Image
import sql
from functions import extract_snowflake_noload, convert_df
from datetime import date
import plotly.express as px

today = date.today()
today_formatted = today.strftime('%Y%m%d')

st.sidebar.markdown("# Portfolio")

image = Image.open('Holaluz_Logo_RGB_Gradient-.png')
image_ns = image.resize([int(0.11 * s) for s in image.size])
st.image(image_ns)
st.title('Portfolio')
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

portfolio_last_15_days = extract_snowflake_noload(sql.QUERY_PORTFOLIO_LAST15_DAYS)
portfolio_last_15_days.rename(columns={'portfolio': 'Portfolio', 'fecha': 'Date'}, inplace=True)

#portfolio_last_15_days.loc[:, "Portfolio"] = portfolio_last_15_days["Portfolio"].map('{:,d}'.format)

col1, col2 = st.columns(2)
col1.dataframe(portfolio_last_15_days)

fig = px.line(portfolio_last_15_days, x='Date', y='Portfolio', markers=True, color_discrete_sequence=['#F06B18'],
              width=600, height=400)
fig.update_yaxes(categoryorder="category ascending")
col2.plotly_chart(fig)

csv_portfolio = convert_df(portfolio_last_15_days)

st.download_button(
   "Download",
   csv_portfolio,
   f"Portfolio_{today_formatted}.csv",
   "text/csv",
   key='download-csv'
)

st.markdown("""---""")
st.subheader('Actual portfolio by product')
portfolio_product = extract_snowflake_noload(sql.QUERY_PORTFOLIO_PRODUCT)
portfolio_product.rename(columns={'portfolio': 'Portfolio', 'product_classification': 'Product'}, inplace=True)
fig_port_prod = px.bar(portfolio_product, x='Product', y='Portfolio', color_discrete_sequence=['#FFC621'],
              width=600, height=400)
fig_port_prod.update_yaxes(categoryorder="category ascending")

st.plotly_chart(fig_port_prod)
csv_portfolio_prod = convert_df(portfolio_product)

st.download_button(
   "Download",
   csv_portfolio_prod,
   f"Portfolio_Product_{today_formatted}.csv",
   "text/csv",
   key='download-csv-port'
)