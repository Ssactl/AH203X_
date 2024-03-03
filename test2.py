import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from st_files_connection import FilesConnection


# df_location=pd.read_csv(f'../../3.Data/OneDrive - KTH/GTFS Data/stops_2022.csv')
# df = pd.read_csv(f'../../3.Data/OneDrive - KTH/GTFS Data/avl_data_corrected_2022_05.csv', header = 0)

url="https://docs.google.com/spreadsheets/d/1m1hFLiERBIMYdgG7BMrude3eupMY_mZA0qFTifG39rk/edit?usp=drive_link"
conn = st.connection("gsheets", type=GSheetsConnection)
df_location = conn.read(spreadsheet=url)
st.dataframe(df_location)

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('gcs', type=FilesConnection)
df = conn.read("streamlit_app_buckt/avl_data_corrected_2022_05.csv",input_format="csv")
