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
# st.dataframe(df_location)

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('gcs', type=FilesConnection)
df = conn.read("streamlit_app_buckt/avl_data_corrected_2022_05.csv",input_format="csv")
# st.dataframe(df)

st.markdown('<style>body { font-size: 18px; }</style>', unsafe_allow_html=True)

# # Streamlit App
st.title('1 数据处理')


#################################################################################################################
####################### 1.1 选区域
#################################################################################################################

st.header('1.1 选区域')

# 矩形区域的坐标
min_lat, max_lat = min([59.371219, 59.318553]), max([59.371219, 59.318553])
min_lon, max_lon = min([17.977301, 18.116381]), max([17.977301, 18.116381])

# 使用条件筛选选择位于矩形区域内的站点
df_location_selected = df_location[
    (df_location['lat'] >= min_lat) & (df_location['lat'] <= max_lat) &
    (df_location['lon'] >= min_lon) & (df_location['lon'] <= max_lon)
]

# 通过 'StopAreaNumber' 列获取站点 ID 列表
selected_sans = df_location_selected['StopAreaNumber'].tolist()
# 从 GTFS 数据中选择 'to_stop_san' 列值在选定站点 ID 列表中的数据
df_selected= df[df['to_stop_san'].isin(selected_sans)]

# 将 'to_stop_san' 列的唯一值创建为 DataFrame
all_stops = pd.DataFrame(df['to_stop_san'].unique(), columns=['to_stop_san'])
# 合并数据框
all_stops = pd.merge(all_stops, df_location[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')
st.text(f'站点数量：{len(all_stops)}')
# 删除 'to_stop' 列中的 NaN 值
all_stops = all_stops.dropna()
st.text(f'删匹配不到经纬度的站点之后 站点数量：{len(all_stops)}')

st.text(f'所有站点 空间分布图:')
st.map(all_stops, latitude='lat', longitude='lon',size=8, color='#e74c3c')

st.text(f'以[59.371219, 17.977301], [59.318553, 18.116381] 这两点确定一个矩形区域')

selected_stops=all_stops[all_stops['to_stop_san'].isin(selected_sans)]
st.text(f'筛选出在该区域内的 站点数量：{len(selected_stops)}')

st.text(f'选定区域内 站点 空间分布图:')
st.map(selected_stops, latitude='lat', longitude='lon',size=8, color='#e74c3c')

#################################################################################################################
####################### 2.1 
#################################################################################################################

st.header('2.1 ')

df_selected=df_selected[["CalendarDateKey","avl_delay",'to_stop_san','tosan_observed_arrival_time_sfm']]
st.dataframe(df_selected.describe())

st.text(f'The tosan_observed_arrival_time_sfm contains 14 null values. And it ranges from -2.000 to 83289.000 seconds. This means that there are stations that still have buses arriving as early as 00:00:00 and stations that still have buses arriving as late as 23:08:09.')

#################################################################################################################
####################### 2.1.2 "tosan_observed_arrival_time_sfm" 
#################################################################################################################

st.subheader('2.1.2 "tosan_observed_arrival_time_sfm" ')

st.text(f'tosan_observed_arrival_time_sfm 14个空值，先直接drop掉')
df_selected = df_selected.dropna(subset=['tosan_observed_arrival_time_sfm'])

#################################################################################################################
####################### 2.1.3 analysis of "avl_delay" 
#################################################################################################################

st.subheader('2.1.3 analysis of "avl_delay"')
st.dataframe(df_selected.describe())
st.text(f'The avl_delay ranges between -11045.000	seconds and 9604.000 seconds. This means that there was a bus that arrived approximately 184 minutes (3 hours) early, but also that there was a bus that arrived nearly 160 minutes (3.2 hours) late. On average the busses arrived 120.152	seconds, approximately 2 minutes late.')

#################################################################################################################
####################### 2.1.3.1 Null values
#################################################################################################################

st.markdown('### 2.1.3.1 Null values')

st.text(f'avl_delay 有 373174 个空值, 总体大约有18.1%的空值，看下各站点的空值占比和空间分布')

# 每个站点的 avl_delay 列的空值占该站点数据的百分比
null_values_percentage_by_stop = df_selected['avl_delay'].isnull().groupby(df_selected['to_stop_san']).mean() * 100
# 合并数据框
null_values_percentage_by_stop  = pd.merge(null_values_percentage_by_stop, df_location_selected[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left').rename(columns={'avl_delay': 'NullValuesPercentage'})

st.text('null_values_percentage histogram:')
fig_hist = px.histogram(null_values_percentage_by_stop, x='NullValuesPercentage', nbins=20, title=f'Distribution of Null Values Percentage by Stop')
st.plotly_chart(fig_hist)

st.text(f'null_values_percentage 空间分布图:')
fig_map = px.scatter_mapbox(null_values_percentage_by_stop, lat='lat', lon='lon', size=[2] * len(null_values_percentage_by_stop),color='NullValuesPercentage',
                            color_continuous_scale='emrld', zoom=10, mapbox_style='carto-positron',hover_data=['StopAreaNumber', 'StopAreaName'])
# 调整悬停文本的字体大小
fig_map.update_layout(hoverlabel_font_size=16)  # 设置为适当的字体大小
st.plotly_chart(fig_map)

st.text(f'317个0%, 25个100%，直接删空值')

df_selected = df_selected.dropna(subset=['avl_delay'])

#################################################################################################################
####################### 2.1.3.2 The avl_delay values:   
#################################################################################################################

st.markdown('### 2.1.3.2 The avl_delay values:')

# 将日期和时间列转换为日期时间格式
df_selected['date'] = pd.to_datetime(df_selected['CalendarDateKey'], format='%Y%m%d')
# 将秒数转换为 timedelta
df_selected['time'] = pd.to_timedelta(df_selected['tosan_observed_arrival_time_sfm'], unit='s')
# 合并日期和时间列
df_selected['datetime'] = df_selected['date'] + df_selected['time']
# 获取星期
df_selected['weekday'] = df_selected['datetime'].dt.weekday
# 分箱，例如按小时分箱
df_selected['hour'] = df_selected['datetime'].dt.hour

####################### avl_delay histogram #######################
st.text('avl_delay histogram:')
fig_hist = px.histogram(df_selected, x='avl_delay', nbins=300, title=f'Distribution of AVL Delay')
st.plotly_chart(fig_hist)

early_arrival_percentage = (df_selected[df_selected['avl_delay'] < 0]['avl_delay']
                            .count() / df_selected['avl_delay'].count() * 100)
st.text(f'avl_delay 早到占比: {early_arrival_percentage:.2f}%')

early_arrival_percentage_1_min = (df_selected[(df_selected['avl_delay'] < 0) & (df_selected['avl_delay'] > -60)]['avl_delay'].count() / df_selected['avl_delay'].count() * 100)
st.text(f"avl_delay 早到小于1分钟占比: {early_arrival_percentage_1_min:.2f}%")

early_arrival_percentage_greater_10_min = (df_selected[(df_selected['avl_delay'] < -600)]['avl_delay'].count() / df_selected['avl_delay'].count() * 100)
st.text(f"avl_delay 早到大于10分钟占比: {early_arrival_percentage_greater_10_min:.2f}%")

st.text(f"   ")

# 选择站点并显示 delay 直方图
selectbox_stops = st.multiselect('选择站点查看 Delay 直方图:', df_selected['to_stop_san'].unique())
if selectbox_stops:
    st.text(f'{selectbox_stops} 站点 Delay 直方图:')
    for selected_stop in selectbox_stops:
        selectbox_stop_data = df_selected[df_selected['to_stop_san'] == selected_stop]
        fig_hist = px.histogram(selectbox_stop_data, x='avl_delay', nbins=20, title=f'Distribution of Delay at {selected_stop}')
        st.plotly_chart(fig_hist)
else:
    st.text("请选择一个或多个站点查看 Delay 直方图.")

####################### 根据站点计算 delay 均值 #######################
    
def draw_stop_delay_h_and_m(title,data, st_write, column_name):
    # st.text(f'站点 {st_write} 直方图：')
    fig_hist = px.histogram(data, x=column_name, nbins=20, title=title)
    st.plotly_chart(fig_hist)
    
    # st.text(f'站点 {st_write} 空间分布图:')
    fig_map = px.scatter_mapbox(data, lat='lat', lon='lon', size=[2] * len(data), color=column_name,
                                 color_continuous_scale='picnic', color_continuous_midpoint=0, zoom=10, mapbox_style='carto-positron',custom_data = ['StopAreaNumber','StopAreaName',column_name])
    # 设置悬浮标签字体大小
    fig_map.update_layout(hoverlabel_font_size=16)  # 设置为适当的字体大小
    fig_map.update_traces(hovertemplate='%{customdata[0]}<br>%{customdata[1]}<br>%{customdata[2]:.2f}')

    st.plotly_chart(fig_map)


st.markdown('#### 站点 delay均值')

average_delay_by_stop =  df_selected.groupby(['to_stop_san'])['avl_delay'].mean().reset_index().rename(columns={'avl_delay':'average_delay'}).fillna(0)
st.dataframe(average_delay_by_stop.describe())
average_delay_by_stop  = pd.merge(average_delay_by_stop , df_location_selected[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')

draw_stop_delay_h_and_m(f'Distribution of Average Delay by Stop',average_delay_by_stop,'delay均值', 'average_delay')

st.write(f'https://ssactl.github.io/AH203X_/average_delay_by_stop_map.html')
# 读取 HTML 文件内容
# file_path = f'../2.code/results/average_delay_by_stop_map.html'
file_path = f'average_delay_by_stop_map.html'
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()
# 将 HTML 内容嵌入到 Streamlit 中
html(html_content, height=600)


##### 计算每个站点 delay 小于0 的占比
st.markdown('#### 站点 delay小于0的占比')
early_arrival_percentage_by_stop = (df_selected[df_selected['avl_delay'] < 0]
                             .groupby('to_stop_san')['avl_delay']
                             .count() / df_selected.groupby('to_stop_san')['avl_delay'].count() * 100).reset_index().rename(columns={'avl_delay': 'EarlyArrivalPercentage'}).fillna(0)

st.dataframe(early_arrival_percentage_by_stop.describe())

early_arrival_percentage_by_stop = pd.merge(early_arrival_percentage_by_stop, df_location_selected[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')

draw_stop_delay_h_and_m(f'Distribution of Stations with Early Arrival Percentage',early_arrival_percentage_by_stop,'delay小于0的占比','EarlyArrivalPercentage')
 
####################### 计算每个站点早到1分钟的占比 #######################
st.markdown('#### 站点 早到1分钟(delay小于0大于-60) 的占比')
early_arrival_percentage_1_min_by_stop = (
    df_selected[(df_selected['avl_delay'] < 0) & (df_selected['avl_delay'] >= -60)]
     .groupby('to_stop_san')['avl_delay']
     .count() / df_selected.groupby('to_stop_san')['avl_delay'].count() * 100
).reset_index().rename(columns={'avl_delay': 'EarlyArrivalPercentageOneMin'}).fillna(0)

st.dataframe(early_arrival_percentage_1_min_by_stop.describe())

early_arrival_percentage_1_min_by_stop = pd.merge(early_arrival_percentage_1_min_by_stop, df_location_selected[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')

draw_stop_delay_h_and_m(f'Distribution of Early Arrival Percentage (Less than 1 minute) by Stop',early_arrival_percentage_1_min_by_stop,'早到1分钟的占比', 'EarlyArrivalPercentageOneMin')

####################### 每个站点 早到1分钟占各站点所有早到 的占比 #######################
st.markdown('#### 每个站点 早到1分钟 占各站点所有早到 的占比')
early_arrival_percentage_one_min_to_all_early_arrivals_by_stop = (df_selected[(df_selected['avl_delay'] < 0) & (df_selected['avl_delay'] > -60)]
                                     .groupby('to_stop_san')['avl_delay']
                                     .count() / df_selected[df_selected['avl_delay'] < 0].groupby('to_stop_san')['avl_delay'].count() * 100).reset_index().rename(columns={'avl_delay': 'EarlyArrivalPercentageOneMinuteToAllEarlyArrival'}).fillna(0)

st.dataframe(early_arrival_percentage_one_min_to_all_early_arrivals_by_stop.describe())

early_arrival_percentage_one_min_to_all_early_arrivals_by_stop = pd.merge(early_arrival_percentage_one_min_to_all_early_arrivals_by_stop, df_location_selected[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')

draw_stop_delay_h_and_m(f'Distribution of Early Arrival Percentage (Less than 1 minute) To All Early Arrivals by Stop',early_arrival_percentage_one_min_to_all_early_arrivals_by_stop,'早到1分钟占各站点所有早到占比', 'EarlyArrivalPercentageOneMinuteToAllEarlyArrival')

####################### 早到10分钟以上的占比 #######################
st.markdown('#### 每个站点 早到超过10分钟 的占比')
early_arrival_percentage_greater_ten_min_by_stop = (df_selected[df_selected['avl_delay'] < -600]
                             .groupby('to_stop_san')['avl_delay']
                             .count() / df_selected.groupby('to_stop_san')['avl_delay'].count() * 100).reset_index().rename(columns={'avl_delay': 'EarlyArrivalPercentage_GreaterTenMin'}).fillna(0)

st.dataframe(early_arrival_percentage_greater_ten_min_by_stop.describe())

early_arrival_percentage_greater_ten_min_by_stop = pd.merge(early_arrival_percentage_greater_ten_min_by_stop, df_location_selected[['StopAreaNumber', 'lon', 'lat','StopAreaName']], left_on='to_stop_san', right_on='StopAreaNumber', how='left')

draw_stop_delay_h_and_m(f'Distribution of Early Arrival Percentage (More than 10 minute) by Stop',early_arrival_percentage_greater_ten_min_by_stop,'早到超过10分钟占比', 'EarlyArrivalPercentage_GreaterTenMin')

