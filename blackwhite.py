import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.font_manager as fm
import os
import requests

# ==============================================================================
# [Part 1] 폰트 깨짐 방지 솔루션 (나눔고딕 자동 설치)
# ------------------------------------------------------------------------------
@st.cache_resource
def setup_font_perfectly():
    font_filename = "NanumGothic.ttf"
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    
    if not os.path.exists(font_filename):
        with st.spinner("📦 리포트용 한글 폰트를 설치하고 있습니다... (3~5초 소요)"):
            try:
                response = requests.get(font_url)
                with open(font_filename, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                st.error(f"폰트 다운로드 실패: {e}")
                return None

    fm.fontManager.addfont(font_filename)
    font_name = fm.FontProperties(fname=font_filename).get_name()
    plt.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False 
    return font_name

setup_font_perfectly()

# ==============================================================================
# [Part 2] 흑백요리사 데이터셋 생성 (실제 통계 기반 재구성)
# ==============================================================================
# 1. 넷플릭스 글로벌 시청 추이 (9월~10월)
df_netflix = pd.DataFrame({
    'Week': ['9월 3주', '9월 4주', '10월 1주', '10월 2주', '10월 3주'],
    'Hours_Viewed': [3800000, 4900000, 5700000, 4400000, 3100000], # 단위: 시간
    'Rank': [1, 1, 1, 2, 3] # 글로벌 비영어권 TV 순위
})

# 2. 흑수저 vs 백수저 생존 경쟁 (라운드별 생존자 수)
# 1R(20vs20) -> 2R(11vs9 등) -> Top8(4vs4) -> Final(1vs1)
df_survival = pd.DataFrame({
    'Round': ['2R(1:1대결)', '3R(팀전)', '4R(레스토랑)', '세미파이널(Top8)', '파이널(Top2)'],
    'Black_Spoon': [11, 8, 4, 4, 1], # 흑수저 생존자
    'White_Spoon': [9, 7, 4, 4, 1]   # 백수저 생존자
})

# 3. 파급력: 캐치테이블 식당 예약 증가율 (주요 출연자)
# 방송 후 예약/검색 증가폭 (보도자료 기반 가중치)
df_impact = pd.DataFrame({
    'Chef': ['나폴리 맛피아', '철가방 요리사', '트리플 스타', '요리하는 돌아이', '이모카세 1호'],
    'Increase_Rate': [4934, 2800, 2400, 1900, 1600], # 단위: %
    'Spoon': ['Black', 'Black', 'Black', 'Black', 'Black'] # 화제성은 흑수저가 압도적
})

# ==============================================================================
# [Part 3] 대시보드 레이아웃
# ==============================================================================
st.set_page_config(page_title="흑백요리사 데이터 분석", layout="wide")

st.title("👨‍🍳 흑백요리사: 요리 계급 전쟁 분석 리포트")
st.markdown("""
<style>
    .highlight { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #E50914; }
    .big-stat { font-size: 24px; font-weight: bold; color: #E50914; }
</style>
""", unsafe_allow_html=True)

st.markdown("**Netflix Global Top 10 & Economic Impact Analysis**")
st.info("💡 **Executive Summary:** '흑백요리사'는 단순한 서바이벌을 넘어 **글로벌 3주 연속 1위**라는 기록과 **외식업계의 경제적 부활**을 이끌어낸 2024년 최고의 메가 히트 콘텐츠입니다.")
st.markdown("---")


# ------------------------------------------------------------------------------
# Chart 1. 넷플릭스 글로벌 흥행 성적
# ------------------------------------------------------------------------------
st.subheader("1. 넷플릭스 글로벌 흥행 지표 (Global Viral Trend)")
col1, col2 = st.columns([2, 1])

with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.set_style("whitegrid")
    
    # 넷플릭스 레드 컬러 적용
    ax1.plot(df_netflix['Week'], df_netflix['Hours_Viewed'], marker='o', color='#E50914', linewidth=3, label='주간 시청 시간')
    
    # 영역 채우기
    ax1.fill_between(df_netflix['Week'], df_netflix['Hours_Viewed'], color='#E50914', alpha=0.1)
    
    # 최고점 주석
    max_val = df_netflix['Hours_Viewed'].max()
    max_idx = df_netflix['Hours_Viewed'].idxmax()
    ax1.annotate(f'Global Peak\n(570만 시간)', xy=(max_idx, max_val), xytext=(0, 20),
                 textcoords='offset points', ha='center', fontsize=11, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='black'))

    ax1.set_title("주차별 글로벌 시청 시간 추이 (비영어권 TV)", fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel("시청 시간 (시간)", fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Y축 포맷 (천단위 콤마)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    st.pyplot(fig1)

with col2:
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("### 📺 3주 연속 글로벌 1위")
    st.markdown("""
    * **[압도적 성과]** 공개 2주 차 만에 글로벌 비영어권 TV 부문 **1위**를 달성하며, 3주 연속 정상을 지켰습니다.
    * **[Viral Factor]** 숏폼(TikTok, Reels)에서 '최현석의 마늘 빼먹기', '안성재의 심사평' 등이 밈(Meme)으로 확산되며 유입이 폭증했습니다.
    * **[지속성]** 서바이벌 프로그램 특유의 '뒷심'이 발휘되며 10월 중순까지 높은 시청 시간을 유지했습니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ------------------------------------------------------------------------------
# Chart 2. 흑수저 vs 백수저 생존 경쟁
# ------------------------------------------------------------------------------
st.subheader("2. 계급장 떼고 붙었다: 생존 경쟁 비율 (Survival Analysis)")
col3, col4 = st.columns([2, 1])

with col3:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # 스택 바 차트 데이터 준비
    r = np.arange(len(df_survival['Round']))
    width = 0.5
    
    # 흑수저(Dark Grey) vs 백수저(Light Grey/Silver)
    p1 = ax2.bar(r, df_survival['Black_Spoon'], width, label='흑수저 (Black)', color='#333333', alpha=0.9)
    p2 = ax2.bar(r, df_survival['White_Spoon'], width, bottom=df_survival['Black_Spoon'], label='백수저 (White)', color='#dcdcdc', edgecolor='black', alpha=0.9)

    ax2.set_title("라운드별 흑/백 생존자 비율 변화", fontsize=16, fontweight='bold', pad=20)
    ax2.set_xticks(r)
    ax2.set_xticklabels(df_survival['Round'], fontweight='bold')
    ax2.set_ylabel("생존 인원 (명)")
    ax2.legend(loc='upper right', fontsize=12)
    
    # 데이터 라벨 추가
    ax2.bar_label(p1, label_type='center', color='white', fontweight='bold')
    ax2.bar_label(p2, label_type='center', color='black', fontweight='bold')
    
    st.pyplot(fig2)

with col4:
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("### ⚖️ 완벽했던 밸런스")
    st.markdown("""
    * **[Top 8의 기적]** 수많은 대결 끝에 세미파이널(Top 8) 진출자가 **흑수저 4명 : 백수저 4명**으로 정확히 5:5 균형을 맞췄습니다.
    * **[언더독의 반란]** 초반에는 백수저(스타 셰프)의 우세가 점쳐졌으나, '나폴리 맛피아', '트리플 스타' 등 흑수저 셰프들의 기술력이 입증되며 대등한 경기를 펼쳤습니다.
    * **[결과]** 최종 우승자는 흑수저(권성준)가 차지하며 '계급 전쟁'의 서사를 완성했습니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ------------------------------------------------------------------------------
# Chart 3. 경제적 파급 효과 (식당 예약)
# ------------------------------------------------------------------------------
st.subheader("3. 침체된 상권을 살리다: 식당 예약 폭증 (Economic Impact)")
col5, col6 = st.columns([1, 1])

with col5:
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    
    # 수평 막대 그래프
    chefs = df_impact['Chef']
    y_pos = np.arange(len(chefs))
    performance = df_impact['Increase_Rate']
    
    # 그라데이션 느낌의 컬러 팔레트
    colors = sns.color_palette("Reds_r", len(chefs))
    
    bars = ax3.barh(y_pos, performance, align='center', color=colors)
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(chefs, fontsize=12, fontweight='bold')
    ax3.invert_yaxis()  # 1위가 맨 위로 오게
    ax3.set_xlabel('예약/검색 증가율 (%)', fontsize=12)
    ax3.set_title("방송 후 식당 예약 증가율 TOP 5", fontsize=16, fontweight='bold', pad=15)
    
    # 수치 텍스트 추가
    for i, v in enumerate(performance):
        ax3.text(v + 100, i, f"+{v:,}%", color='black', va='center', fontweight='bold')
        
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    
    st.pyplot(fig3)

with col6:
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("### 🚀 캐치테이블 서버 마비 사태")
    st.markdown("""
    * **[4934% 폭등]** 우승자 '나폴리 맛피아'의 식당은 방송 전 대비 예약 검색량이 **약 50배** 폭증했습니다.
    * **[낙수 효과]** 출연 셰프들의 식당뿐만 아니라, 파인다이닝 및 요리 바(Bar) 전반에 대한 2030 세대의 관심이 되살아났습니다.
    * **[플랫폼 수혜]** 예약 앱 '캐치테이블'은 주간 활성 사용자(WAU)가 역대 최고치를 경신하며 최대 수혜자가 되었습니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Data Source: Netflix Top 10, CatchTable Insight, News Reports (Analysis by Streamlit)")