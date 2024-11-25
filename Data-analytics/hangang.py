import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data():
    """데이터 로드 및 전처리"""
    # 데이터 로드
    data = pd.read_csv('./data/(한강)수난사고 구조출동 현황 2022.csv', encoding='utf-8')
    
    # 컬럼명 소문자로 변환
    data.columns = data.columns.str.lower()
    
    # 숫자형 데이터로 변환
    numeric_cols = ['spt_frstt_dist', 'time_unit_tmprt', 'time_unit_ws', 'time_unit_humidity']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # 시간 데이터 전처리
    data = preprocess_time_data(data)
    
    return data

def preprocess_time_data(data):
    """시간 데이터 전처리"""
    def time_to_minutes(time_str):
        try:
            # 시간 문자열을 6자리로 맞추기
            time_str = str(time_str).zfill(6)
            hours = int(time_str[:2])
            minutes = int(time_str[2:4])
            return hours * 60 + minutes
        except:
            return np.nan

    # 시간 컬럼을 분으로 변환
    data['dsp_time'] = data['dsp_tm'].apply(time_to_minutes)
    data['arvl_time'] = data['spt_arvl_tm'].apply(time_to_minutes)
    data['cmptn_time'] = data['resc_cmptn_tm'].apply(time_to_minutes)
    
    # 소요 시간 계산
    data['avrl_dpt'] = data['arvl_time'] - data['dsp_time']
    data['resc_avrl'] = data['cmptn_time'] - data['arvl_time']
    
    # 비정상 값 처리
    data.loc[data['avrl_dpt'] < 0, 'avrl_dpt'] = np.nan
    data.loc[data['resc_avrl'] < 0, 'resc_avrl'] = np.nan
    
    # 이상치 제거
    data.loc[data['avrl_dpt'] > 120, 'avrl_dpt'] = np.nan  # 2시간 초과
    data.loc[data['resc_avrl'] > 240, 'resc_avrl'] = np.nan  # 4시간 초과
    
    return data

def create_correlation_analysis(data):
    """상관관계 분석 및 시각화"""
    # 분석할 컬럼 선택
    cols = ['avrl_dpt', 'resc_avrl', 'spt_frstt_dist', 
            'time_unit_tmprt', 'time_unit_ws', 'time_unit_humidity']
    
    # 결측치 제거
    analysis_data = data[cols].dropna()
    
    # 상관관계 계산
    corr = analysis_data.corr()
    
    # 히트맵 생성
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, 
                annot=True, 
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                square=True)
    
    plt.title('구조 시간 관련 변수 상관관계')
    return plt.gcf()

def create_scatter_plots(data):
    """산점도 그래프 생성"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '거리와 도착시간',
            '기온과 구조시간',
            '풍속과 구조시간',
            '습도와 구조시간'
        )
    )
    
    # 결측치 제거
    plot_data = data.dropna(subset=['avrl_dpt', 'resc_avrl', 'spt_frstt_dist', 
                                   'time_unit_tmprt', 'time_unit_ws', 'time_unit_humidity'])
    
    # 1. 거리와 도착시간
    fig.add_trace(
        go.Scatter(x=plot_data['spt_frstt_dist'], 
                  y=plot_data['avrl_dpt'],
                  mode='markers',
                  name='거리-도착시간'),
        row=1, col=1
    )
    
    # 2. 기온과 구조시간
    fig.add_trace(
        go.Scatter(x=plot_data['time_unit_tmprt'], 
                  y=plot_data['resc_avrl'],
                  mode='markers',
                  name='기온-구조시간'),
        row=1, col=2
    )
    
    # 3. 풍속과 구조시간
    fig.add_trace(
        go.Scatter(x=plot_data['time_unit_ws'], 
                  y=plot_data['resc_avrl'],
                  mode='markers',
                  name='풍속-구조시간'),
        row=2, col=1
    )
    
    # 4. 습도와 구조시간
    fig.add_trace(
        go.Scatter(x=plot_data['time_unit_humidity'], 
                  y=plot_data['resc_avrl'],
                  mode='markers',
                  name='습도-구조시간'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True)
    return fig

def create_dashboard(data):
    st.title('한강 수난사고 분석 대시보드')
    
    # 기존 시각화 섹션
    st.header('📊 기본 통계 분석')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('월별 사고 발생 현황')
        monthly_fig = create_monthly_incidents(data)
        st.plotly_chart(monthly_fig)
    
    with col2:
        st.subheader('시간대별 사고 발생 현황')
        hourly_fig = create_hourly_incidents(data)
        st.plotly_chart(hourly_fig)
    
    st.header('🗺️ 지역별 분석')
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader('구별 사고 발생 현황')
        district_fig = create_district_incidents(data)
        st.plotly_chart(district_fig)
    
    with col4:
        st.subheader('사고 유형별 분포')
        type_fig = create_incident_types(data)
        st.plotly_chart(type_fig)
    
    # 새로운 시각화 섹션 추가
    st.header('🕒 구조 시간 분석')
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader('상관관계 분석')
        correlation_fig = create_correlation_analysis(data)
        st.pyplot(correlation_fig)
    
    with col6:
        st.subheader('환경 요인과 구조 시간')
        scatter_fig = create_scatter_plots(data)
        st.plotly_chart(scatter_fig)

def create_monthly_incidents(data):
    monthly_counts = data['dsp_mnth'].value_counts().sort_index()
    
    fig = go.Figure(data=[
        go.Bar(x=monthly_counts.index, 
               y=monthly_counts.values,
               text=monthly_counts.values,
               textposition='auto')
    ])
    
    fig.update_layout(
        xaxis_title='월',
        yaxis_title='사고 건수',
        showlegend=False
    )
    
    return fig

def create_hourly_incidents(data):
    hourly_counts = data['dsp_hour'].value_counts().sort_index()
    
    fig = go.Figure(data=[
        go.Bar(x=hourly_counts.index, 
               y=hourly_counts.values,
               text=hourly_counts.values,
               textposition='auto')
    ])
    
    fig.update_layout(
        xaxis_title='시간',
        yaxis_title='사고 건수',
        showlegend=False
    )
    
    return fig

def create_district_incidents(data):
    district_counts = data['sigungu_nm'].value_counts().head(10)
    
    fig = go.Figure(data=[
        go.Bar(x=district_counts.index, 
               y=district_counts.values,
               text=district_counts.values,
               textposition='auto')
    ])
    
    fig.update_layout(
        xaxis_title='구',
        yaxis_title='사고 건수',
        showlegend=False
    )
    
    return fig

def create_incident_types(data):
    type_counts = data['prcs_result_se_nm'].value_counts()
    
    fig = go.Figure(data=[go.Pie(labels=type_counts.index, 
                                values=type_counts.values,
                                hole=.3)])
    
    fig.update_layout(showlegend=True)
    
    return fig

def main():
    data = load_data()
    create_dashboard(data)

if __name__ == "__main__":
    main()