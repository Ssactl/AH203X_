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

# # Create connection object and retrieve file contents.
# # Specify input format is a csv and to cache the result for 600 seconds.
# conn = st.connection('gcs', type=FilesConnection)
# df = conn.read("streamlit_app_buckt/avl_data_corrected_2022_05.csv",input_format="csv")

# st.dataframe(df)

# st.dataframe(df_location)
# # Create a connection object.
# conn = st.connection("gsheets_stops_2022", type=GSheetsConnection)
# df_location = conn.read()

# conn = st.connection("gsheets_avl_data_corrected_2022_05", type=GSheetsConnection)
# df = conn.read()



# df = pd.read_csv(f'../../3.Data/OneDrive - KTH/GTFS Data/avl_data_corrected_2022_05.csv', header = 0)
# df=df[["CalendarDateKey","avl_delay",'to_stop_san','tosan_observed_arrival_time_sfm']]

# df_location=pd.read_csv(f'../../3.Data/OneDrive - KTH/GTFS Data/stops_2022.csv')

# # 矩形区域的坐标
# min_lat, max_lat = min([59.371219, 59.318553]), max([59.371219, 59.318553])
# min_lon, max_lon = min([17.977301, 18.116381]), max([17.977301, 18.116381])

# # 使用条件筛选选择位于矩形区域内的站点
# df_location_selected = df_location[
#     (df_location['lat'] >= min_lat) & (df_location['lat'] <= max_lat) &
#     (df_location['lon'] >= min_lon) & (df_location['lon'] <= max_lon)
# ]

# # 通过 'StopAreaNumber' 列获取站点 ID 列表
# selected_sans = df_location_selected['StopAreaNumber'].tolist()
# # 从 GTFS 数据中选择 'to_stop_san' 列值在选定站点 ID 列表中的数据
# df_selected= df[df['to_stop_san'].isin(selected_sans)]

# # 将 'to_stop_san' 列的唯一值创建为 DataFrame
# all_stops = pd.DataFrame(df['to_stop_san'].unique(), columns=['to_stop_san'])
# # 合并数据框
# all_stops = pd.merge(all_stops, df_location[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')

# # 删除 'to_stop' 列中的 NaN 值
# all_stops = all_stops.dropna()

# selected_stops=all_stops[all_stops['to_stop_san'].isin(selected_sans)]

# df_selected=df_selected[["CalendarDateKey","avl_delay",'to_stop_san','tosan_observed_arrival_time_sfm']]

# df_selected.to_excel('avl_data_corrected_2022_05_selected.xlsx')



