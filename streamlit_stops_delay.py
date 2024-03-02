import streamlit as st
import pandas as pd
import plotly.express as px


merged_data=pd.read_csv('E:\\Degree Project\\0.AH203X_Degree_Project\\2.code\\results\\stops_delay_05.csv')
df_selected=pd.read_csv('E:\\Degree Project\\0.AH203X_Degree_Project\\2.code\\results\\df_selected_05.csv')

# Streamlit App
st.title('站点 Delay 可视化面板')

# Streamlit App
st.title('站点 Delay 可视化面板')
# 显示各站点均值和早到一分钟占比
st.write('各站点均值和早到占比:')
st.dataframe(merged_data)

# 创建站点地图
st.write('站点空间分布图:')
fig_map = px.scatter_mapbox(merged_data, lat='lat', lon='lon', size='EarlyArrivalPercentage', color='average_delay',
                            color_continuous_scale='RdBu_r', size_max=15, zoom=10, mapbox_style='carto-positron')
st.plotly_chart(fig_map)

# 选择站点并显示 delay 直方图
selectbox_stops = st.multiselect('选择站点查看 Delay 直方图:', merged_data['to_stop_san'].unique())
if selectbox_stops:
    st.write(f'{selectbox_stops} 站点 Delay 直方图:')
    for selected_stop in selectbox_stops:
        selectbox_stop_data = df_selected[df_selected['to_stop_san'] == selected_stop]
        fig_hist = px.histogram(selectbox_stop_data, x='avl_delay', nbins=20, title=f'Distribution of Delay at {selected_stop}')
        st.plotly_chart(fig_hist)
else:
    st.write("请选择一个或多个站点查看 Delay 直方图.")

