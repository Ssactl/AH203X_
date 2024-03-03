import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import plotly.express as px
from streamlit_gsheets import GSheetsConnection


# df_location=pd.read_csv(f'../../3.Data/OneDrive - KTH/GTFS Data/stops_2022.csv')
# df = pd.read_csv(f'../../3.Data/OneDrive - KTH/GTFS Data/avl_data_corrected_2022_05.csv', header = 0)

url="https://docs.google.com/spreadsheets/d/1m1hFLiERBIMYdgG7BMrude3eupMY_mZA0qFTifG39rk/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)
df_location = conn.read(spreadsheet=url)

st.dataframe(df_location)
# # Create a connection object.
# conn = st.connection("gsheets_stops_2022", type=GSheetsConnection)
# df_location = conn.read()

# conn = st.connection("gsheets_avl_data_corrected_2022_05", type=GSheetsConnection)
# df = conn.read()
