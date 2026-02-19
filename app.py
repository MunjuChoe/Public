import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="기후변화와 생물다양성", layout="wide")

st.title("🌍 기후변화에 따른 생물다양성 변화 분석")
st.markdown("""
이 앱은 기온 상승이 지구상의 생물다양성에 미치는 영향을 시뮬레이션하고 시각화합니다.
""")

# 2. 가상 데이터 생성 (실제 데이터셋이 있다면 pd.read_csv로 교체 가능)
def load_data():
    years = np.arange(1990, 2026)
    # 기온은 점진적 상승, 생물다양성은 하락하는 경향성 생성
    temp_increase = np.linspace(0, 1.5, len(years)) + np.random.normal(0, 0.1, len(years))
    biodiversity_index = 100 - (temp_increase * 20) + np.random.normal(0, 2, len(years))
    
    df = pd.DataFrame({
        '연도': years,
        '지구평균기온편차': temp_increase,
        '생물다양성지수': biodiversity_index
    })
    return df

df = load_data()

# 3. 사이드바 - 설정
st.sidebar.header("설정 및 필터")
year_range = st.sidebar.slider("조회 기간 선택", 1990, 2025, (1990, 2025))
filtered_df = df[(df['연도'] >= year_range[0]) & (df['연도'] <= year_range[1])]

# 4. 메인 대시보드 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ 기온 변화 추이")
    fig_temp = px.line(filtered_df, x='연도', y='지구평균기온편차', 
                        title="연도별 기온 상승 그래프",
                        line_shape='spline')
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.subheader("🦋 생물다양성 지수 변화")
    fig_bio = px.area(filtered_df, x='연도', y='생물다양성지수', 
                       title="연도별 생물다양성 감소 추세",
                       color_discrete_sequence=['#2ca02c'])
    st.plotly_chart(fig_bio, use_container_width=True)

# 5. 인터랙티브 시뮬레이션 (수정된 부분: --- 대신 st.divider() 사용)
st.divider() 
st.header("🔬 미래 온도 상승 시뮬레이션")
target_temp = st.select_slider(
    "지구 온도가 몇 도 상승한다고 가정할까요?",
    options=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
)



impact_msg = ""
if target_temp >= 2.0:
    impact_msg = "🚨 **심각:** 산호초의 99%가 소실될 위험이 있으며, 많은 포유류의 서식지가 절반 이상 사라집니다."
elif target_temp >= 1.5:
    impact_msg = "⚠️ **주의:** 생계 복원력이 급격히 약화되며, 멸종 속도가 가속화됩니다."
else:
    impact_msg = "✅ **안전:** 생태계가 변화에 적응할 수 있는 최소한의 여유가 있습니다."

st.info(f"온도가 {target_temp}°C 상승할 경우: {impact_msg}")

# 6. 상관관계 분석
st.subheader("📊 기온과 생물다양성의 상관관계")
fig_corr, ax = plt.subplots()
sns.regplot(data=df, x='지구평균기온편차', y='생물다양성지수', ax=ax)
st.pyplot(fig_corr)
