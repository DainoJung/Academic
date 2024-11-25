import matplotlib.pyplot as plt

import numpy as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import folium
from folium.plugins import HeatMap
from matplotlib import font_manager, rc
import platform

#시스템이 window라면 폰트를 '맑은 고딕'으로 설정
if platform.system() == "Windows":
    rc('font', family='Malgun Gothic')
elif platform.system() == "Darwin":  # macOS
    rc('font', family='AppleGothic')
else:  # Linux
    rc('font', family='DejaVu Sans')

plt.rcParams['axes.unicode_minus'] = False  # 음수 부호 설정


# 파일 경로 설정 (Raw 문자열 사용)
file_path_2023 = r'./data/(한강)수난사고 구조출동 현황 2023.csv'
file_path_2022 = r'./data/(한강)수난사고 구조출동 현황 2022.csv'

# CSV 파일 불러오기
data_2023 = pd.read_csv(file_path_2023, encoding='utf-8')
data_2022 = pd.read_csv(file_path_2022, encoding='utf-8')


# In[5]:


# 안쓰는 컬럼 제거 
data_2023 = data_2023.drop([
    'acdnt_cause',
    'prcs_result_se_nm',
    'dclr_ymd',
    'dclr_tm',
    'dclr_yr',
    'qtr_se',
    'dclr_mnth',
    'dclr_day',
    'dclr_hour',
    'dclr_min',
    'spt_arvl_yr',
    'resc_cmptn_yr',
    'hmg_ymd',
    'hmg_tm',
    'hmg_yr',
    'hmg_mnth',
    'hmg_day',
    'hmg_hour',
    'hmg_min',
    'cty_frmvl_se_nm',
    'emd_se_nm',
    'acdnt_place_nm',
    'acdnt_place_detail_nm',
    'frstt_nm',
    'ward_nm',
    'lfdau_nm'
], axis=1)


# In[6]:


data_2022=data_2022.drop([
    'acdnt_cause',
    'prcs_result_se_nm',
    'dclr_ymd',
    'dclr_tm',
    'dclr_yr',
    'qtr_se',
    'dclr_mnth',
    'dclr_day',
    'dclr_hour',
    'dclr_min',
    'spt_arvl_yr',
    'resc_cmptn_yr',
    'hmg_ymd',
    'hmg_tm',
    'hmg_yr',
    'hmg_mnth',
    'hmg_day',
    'hmg_hour',
    'hmg_min',
    'cty_frmvl_se_nm',
    'emd_se_nm',
    'acdnt_place_nm',
    'acdnt_place_detail_nm',
    'frstt_nm',
    'ward_nm',
    'lfdau_nm'
],axis=1)


# In[7]:


# 2023 결측치 있는 행 삭제
data_2023=data_2023.dropna(subset=[
    'dsp_ymd','dsp_tm','dsp_yr', 'dsp_mnth', 'dsp_day','dsp_hour','dsp_min', #출동일자
    'spt_arvl_ymd', # 현장도착일자 (같은 행의 변수들은 생략)
    'resc_cmptn_ymd', # 구조완료 일자
    'spt_frstt_dist', # 현장소방서거리
    'time_unit_tmprt', #시간단위기온
    'time_unit_ws', # 시간단위풍속
    'time_unit_wd', # 시간단위풍향
    'time_unit_humidity', #시간단위습도
    'time_unit', #시간단위가시거리
])


# In[8]:


# 2023 강수량 및 적설량 NULL 값 0으로 대체
# 'time_unit_rainqty'와 'time_unit_msnf'의 결측치를 0으로 대체
data_2023.loc[:, 'time_unit_rainqty'] = data_2023['time_unit_rainqty'].fillna(0)
data_2023.loc[:, 'time_unit_msnf'] = data_2023['time_unit_msnf'].fillna(0)


# In[9]:


# 2022 결측치 있는 행 삭제
data_2022=data_2022.dropna(subset=[
    'dsp_ymd','dsp_tm','dsp_yr', 'dsp_mnth', 'dsp_day','dsp_hour','dsp_min', #출동일자
    'spt_arvl_ymd', # 현장도착일자 (같은 행의 변수들은 생략)
    'resc_cmptn_ymd', # 구조완료 일자
    'gis_x_axis','gis_y_axis', ################ gis x,y 좌표
    'spt_frstt_dist', # 현장소방서거리
])


# In[10]:


# 2022 강수량 및 적설량 NULL 값 0으로 대체
# 'time_unit_rainqty'와 'time_unit_msnf'의 결측치를 0으로 대체
data_2022.loc[:, 'time_unit_rainqty'] = data_2022['time_unit_rainqty'].fillna(0)
data_2022.loc[:, 'time_unit_msnf'] = data_2022['time_unit_msnf'].fillna(0)


# In[11]:


data=pd.concat([data_2023,data_2022])



# 'time_unit_tmprt', 'time_unit_rainqty', 'time_unit_ws', 'time_unit_humidity' 통해 기상 조건에 따른 사고 분석
# 각 기상 조건별로 사고 발생 상황을 평균값으로 분석

# 필요한 열 추출
weather_conditions = data[['acdnt_cause_asort_nm', 'time_unit_tmprt', 'time_unit_rainqty', 'time_unit_ws', 'time_unit_humidity']]

# 각 기상 조건에 따른 사고 원인의 평균 기상 조건 확인
weather_avg_by_cause = weather_conditions.groupby('acdnt_cause_asort_nm').mean()

# 원인에 대한 평균 기상 조건 확인 # 기상 조건에 따른 사고 원인별 평균 기상 분석 결과
weather_avg_by_cause


# In[18]:


# 'season_se_nm' 열을 통해 계절별 수난사고 발생 빈도 분석
season_accident_frequency = data['season_se_nm'].value_counts()

# 계절의 빈도 확인
season_accident_frequency



# In[20]:


# 'season_se_nm', 'time_unit_tmprt', 'time_unit_rainqty', 'time_unit_ws', 'time_unit_humidity'  이용해 
# 계절별 기상 조건과 사고 비교

# 계절별로 평균 기상 조건을 확인하여 사고와 기상 조건 간의 관계 분석

# 필요한 열 추출
season_weather_conditions = data[['season_se_nm', 'time_unit_tmprt', 'time_unit_rainqty', 'time_unit_ws', 'time_unit_humidity']]

# 각 계절별 평균 기상 조건 확인
season_weather_avg = season_weather_conditions.groupby('season_se_nm').mean()

# 계절별 평균 기상 조건
season_weather_avg


# In[21]:


# 'daywk' 열을 통해 요일별 수난사고 발생 빈도 분석
weekday_accident_frequency = data['daywk'].value_counts().sort_index()

# 요일별 수난사고 발생 빈도 확인
weekday_accident_frequency


# In[22]:


# 'time_unit_tmprt', 'time_unit_rainqty', 'time_unit_ws', 'time_unit_humidity' 등을 통해 기상 조건별 사고 빈도 분석
# 기온, 강수량, 풍속, 습도에 따른 사고 발생 빈도를 구간화하여 분석

# 필요한 열 추출
weather_conditions_for_analysis = data[['time_unit_tmprt', 'time_unit_rainqty', 'time_unit_ws', 'time_unit_humidity']].dropna()

# 기온, 강수량, 풍속, 습도에 따른 사고 빈도 구간화
temp_bins = pd.cut(weather_conditions_for_analysis['time_unit_tmprt'], bins=[-10, 0, 10, 20, 30, 40], labels=["<0°C", "0-10°C", "10-20°C", "20-30°C", ">30°C"])
rain_bins = pd.cut(weather_conditions_for_analysis['time_unit_rainqty'], bins=[0, 1, 5, 10, 50, 100], labels=["0-1mm", "1-5mm", "5-10mm", "10-50mm", ">50mm"])
ws_bins = pd.cut(weather_conditions_for_analysis['time_unit_ws'], bins=[0, 2, 4, 6, 8, 10], labels=["0-2m/s", "2-4m/s", "4-6m/s", "6-8m/s", ">8m/s"])
humidity_bins = pd.cut(weather_conditions_for_analysis['time_unit_humidity'], bins=[0, 20, 40, 60, 80, 100], labels=["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"])

# 각 기상 조건별 사고 빈도 계산
weather_conditions_for_analysis['temp_range'] = temp_bins
weather_conditions_for_analysis['rain_range'] = rain_bins
weather_conditions_for_analysis['wind_speed_range'] = ws_bins
weather_conditions_for_analysis['humidity_range'] = humidity_bins

# 기온, 강수량, 풍속, 습도 구간별 사고 빈도 계산
temp_accident_frequency = weather_conditions_for_analysis['temp_range'].value_counts().sort_index()
rain_accident_frequency = weather_conditions_for_analysis['rain_range'].value_counts().sort_index()
ws_accident_frequency = weather_conditions_for_analysis['wind_speed_range'].value_counts().sort_index()
humidity_accident_frequency = weather_conditions_for_analysis['humidity_range'].value_counts().sort_index()




sigungu_nm = data[['sigungu_nm']].value_counts()
sigungu_nm_df = sigungu_nm.reset_index()
sigungu_nm_df




#시간 데이터를 다루기 위한 임의의 데이터프레임 생성
df = pd.DataFrame(data)
tmdata = ['dsp_yr', 'dsp_mnth', 'dsp_day','dsp_hour','dsp_min', 'spt_arvl_mnth','spt_arvl_day', 'spt_arvl_hour','spt_arvl_min',
          'resc_cmptn_mnth', 'resc_cmptn_day','resc_cmptn_hour', 'resc_cmptn_min']
tmdata = df[tmdata]


# In[32]:


#데이터 타입을 'int'로 변경
tmdata['dsp_yr'] = tmdata['dsp_yr'].astype(int)
tmdata['dsp_mnth'] = tmdata['dsp_mnth'].astype(int)
tmdata['dsp_day'] = tmdata['dsp_day'].astype(int)
tmdata['dsp_hour'] = tmdata['dsp_hour'].astype(int)
tmdata['dsp_min'] = tmdata['dsp_min'].astype(int)
tmdata['spt_arvl_mnth'] = tmdata['spt_arvl_mnth'].astype(int)
tmdata['spt_arvl_day'] = tmdata['spt_arvl_day'].astype(int)
tmdata['spt_arvl_hour'] = tmdata['spt_arvl_hour'].astype(int)
tmdata['spt_arvl_min'] = tmdata['spt_arvl_min'].astype(int)
tmdata['resc_cmptn_mnth'] = tmdata['resc_cmptn_mnth'].astype(int)
tmdata['resc_cmptn_day'] = tmdata['resc_cmptn_day'].astype(int)
tmdata['resc_cmptn_hour'] = tmdata['resc_cmptn_hour'].astype(int)
tmdata['resc_cmptn_min'] = tmdata['resc_cmptn_min'].astype(int)


# In[34]:


#datetime으로 사용하려면 초단위 필요, 초 단위의 컬럼 생성
tmdata['sec'] = 0


# ### 출동시간-현장도착시간 계산 후 data에 합치기

# In[35]:


from datetime import datetime, timedelta

dptarvl_list = []

for i in range(0, 8980, 1):
    try:
        #출발시간
        dsp_yr = tmdata['dsp_yr'][i]
        dsp_mnth = tmdata['dsp_mnth'][i]
        dsp_day = tmdata['dsp_day'][i]
        dsp_hour = tmdata['dsp_hour'][i]
        dsp_min = tmdata['dsp_min'][i]
        sec = tmdata['sec'][i]
        dpt = datetime(dsp_yr,dsp_mnth,dsp_day,dsp_hour,dsp_min,sec)
        #print(dpt)

        #도착시간
        arvl_mnth = tmdata['spt_arvl_mnth'][i]
        arvl_day = tmdata['spt_arvl_day'][i]
        arvl_hour = tmdata['spt_arvl_hour'][i]
        arvl_min = tmdata['spt_arvl_min'][i]
        sec = tmdata['sec'][i]
        arvl = datetime(dsp_yr,arvl_mnth,arvl_day,arvl_hour,arvl_min,sec)
        #print(dpt,"-",arvl)

        #시간연산 및 리스트 append
        #print(i, "",arvl - dpt)
        dptarvl = arvl - dpt
        dptarvl_list.append(dptarvl)
    except:
        dptarvl = datetime(2024,1,1,0,0,0) - datetime(2024,1,1,0,0,0)
        dptarvl_list.append(dptarvl)
        continue

#리스트 데이터프레임 추가 및 출력
dptarvl_list = pd.DataFrame(dptarvl_list)
#print(dptarvl_list)
tmdata['avrl_dpt'] = dptarvl_list
#data 데이터프레임에 추가
data['avrl_dpt'] = dptarvl_list
data


# In[36]:


tmdata['avrl_dpt'].value_counts()


# ### 현장도착시간-구조완료시간

# In[37]:


from datetime import datetime, timedelta

arvlresc_list = []

for i in range(0, 8980, 1):
    try:
        #현장도착시간
        arvl_mnth = tmdata['spt_arvl_mnth'][i]
        arvl_day = tmdata['spt_arvl_day'][i]
        arvl_hour = tmdata['spt_arvl_hour'][i]
        arvl_min = tmdata['spt_arvl_min'][i]
        sec = tmdata['sec'][i]
        arvl = datetime(dsp_yr,arvl_mnth,arvl_day,arvl_hour,arvl_min,sec)
        #print(dpt,"-",arvl)

        #구조완료시간
        resc_mnth = tmdata['resc_cmptn_mnth'][i]
        resc_day = tmdata['resc_cmptn_day'][i]
        resc_hour = tmdata['resc_cmptn_hour'][i]
        resc_min = tmdata['resc_cmptn_min'][i]
        sec = tmdata['sec'][i]
        resc = datetime(dsp_yr,resc_mnth,resc_day,resc_hour,resc_min,sec)

        
        #print(i, "",arvl - dpt)
        arvlresc = resc - arvl
        arvlresc_list.append(arvlresc)
    except:
        arvlresc = datetime(2024,1,1,0,0,0) - datetime(2024,1,1,0,0,0)
        arvlresc_list.append(arvlresc)
        continue
        

arvlresc_list = pd.DataFrame(arvlresc_list)
#print(arvlresc_list)
tmdata['resc_avrl'] = arvlresc_list
#data 데이터프레임에 추가
data['resc_avrl'] = arvlresc_list
data




tmdata['resc_avrl'].value_counts()




#데이터 타입 int64로 변화
data['avrl_dpt'] = data['avrl_dpt'].astype(dtype ='int64')
data['resc_avrl'] = data['resc_avrl'].astype(dtype ='int64')
#나노초로 변환된 시간을 다시 '분'단위로 변환
data['avrl_dpt'] = data['avrl_dpt'] / (10**9 * 60)
data['resc_avrl'] = data['resc_avrl'] / (10**9 * 60)



# rainfall intensity
def classify_rainfall(rain_qty):
        if rain_qty == 0:
            return '비 안오는 날'
        elif rain_qty < 3:
            return '약한 비'
        elif rain_qty < 15:
            return '보통 비'
        elif rain_qty < 30:
            return '강한 비'
        else:
            return '매우 강한 비'
    

data['rain_intensity'] = data['time_unit_rainqty'].apply(classify_rainfall)


# In[46]:


data[['time_unit_rainqty', 'rain_intensity']]


# In[47]:


# 각 강수량 강도별 개수 세기
rain_intensity_counts = data['rain_intensity'].value_counts()

# 결과 출력
print(rain_intensity_counts)


# In[48]:


# '비 안오는 날'과 '비 오는 날' 구분
rainy_days_count = len(data[data['rain_intensity'] != '비 안오는 날'])
non_rainy_days_count = len(data[data['rain_intensity'] == '비 안오는 날'])



data[data['rain_intensity'] == '비 안오는 날']




data[data['rain_intensity'] == '약한 비']


# In[53]:


data[data['rain_intensity'] == '보통 비']


# In[54]:


data[data['rain_intensity'] == '강한 비']


# In[55]:


data[data['rain_intensity'] == '매우 강한 비']


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# # 가장 먼저 페이지 설정을 해줍니다
# st.set_page_config(
#     page_title="한강 수난사고 데이터 분석",
#     page_icon="🌊",
#     layout="wide"
# )

# 폰트 설정 등 나머지 코드...
if platform.system() == "Windows":
    rc('font', family='Malgun Gothic')
elif platform.system() == "Darwin":  # macOS
    rc('font', family='AppleGothic')
else:  # Linux
    rc('font', family='DejaVu Sans')

# 제목과 설명
st.title('🌊 한강 수난사고 데이터 분석 대시보드')
st.markdown("""
이 대시보드는 2022-2023년 한강 수난사고 데이터를 분석하여 보여줍니다.
""")

# 데이터 개요 섹션
with st.container():
    st.subheader('📊 데이터 개요')
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("총 사고 건수", f"{len(data):,}건")
    with col2:
        st.metric("분석 기간", "2022-2023년")

# 데이터 미리보기
with st.expander("원본 데이터 미리보기"):
    st.dataframe(data.head(), use_container_width=True)

# 강수량 분석 섹션
st.subheader('☔ 강수량 분석')
col1, col2 = st.columns(2)

with col1:
    # Plotly를 사용한 강수량 강도별 사고 발생 빈도
    rain_counts = data['rain_intensity'].value_counts()
    fig1 = px.bar(
        x=rain_counts.index,
        y=rain_counts.values,
        title='강수량 강도별 사고 발생 빈도',
        labels={'x': '강수량 강도', 'y': '사고 건수'},
        color=rain_counts.values,
        color_continuous_scale='Blues'
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # 강수량과 구조시간 분석
    fig2 = px.box(
        data,
        x='rain_intensity',
        y='resc_avrl',
        title='강수량 강도별 구조 소요시간 분포',
        labels={'rain_intensity': '강수량 강도', 'resc_avrl': '구조 소요시간(분)'},
        color='rain_intensity',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig2, use_container_width=True)

# 계절별 분석 섹션
st.subheader('🍂 계절별 분석')
season_counts = data['season_se_nm'].value_counts()
fig3 = px.pie(
    values=season_counts.values,
    names=season_counts.index,
    title='계절별 사고 발생 비율',
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig3.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig3, use_container_width=True)

# 시간대별 분석
st.subheader('🕒 시간대별 분석')
hourly_accidents = data['dsp_hour'].value_counts().sort_index()
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=hourly_accidents.index,
    y=hourly_accidents.values,
    mode='lines+markers',
    name='시간대별 사고',
    line=dict(color='#1f77b4', width=2),
    fill='tozeroy'
))
fig4.update_layout(
    title='시간대별 사고 발생 현황',
    xaxis_title='시간',
    yaxis_title='사고 건수',
    hovermode='x'
)
st.plotly_chart(fig4, use_container_width=True)

# 사이드바에 필터 추가
with st.sidebar:
    st.header('🔍 데이터 필터')
    selected_season = st.multiselect(
        '계절 선택',
        options=data['season_se_nm'].unique(),
        default=data['season_se_nm'].unique()
    )
    
    selected_rain = st.multiselect(
        '강수량 강도 선택',
        options=data['rain_intensity'].unique(),
        default=data['rain_intensity'].unique()
    )

# 푸터 추가
st.markdown("""---""")
st.markdown("""
<div style='text-align: center'>
    <small>© 2024 한강 수난사고 분석 대시보드 | 데이터 출처: 서울시 소방재난본부</small>
</div>
""", unsafe_allow_html=True)




