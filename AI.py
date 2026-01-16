import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import requests
from math import pi

# ==============================================================================
# [SYSTEM] 폰트 로딩 (무결점 시스템)
# ==============================================================================
@st.cache_resource
def load_and_configure_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-ExtraBold.ttf" 
    font_path = "NanumGothic-ExtraBold.ttf"

    if not os.path.exists(font_path):
        try:
            with st.spinner("💾 AI 데이터베이스 동기화 중..."):
                response = requests.get(font_url)
                with open(font_path, "wb") as f:
                    f.write(response.content)
        except Exception as e:
            return "sans-serif"

    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    
    plt.rcParams['font.family'] = font_name
    plt.rcParams['axes.unicode_minus'] = False
    sns.set(font=font_name, style='darkgrid', rc={"axes.unicode_minus":False})
    
    return font_name

font_name = load_and_configure_font()

# ==============================================================================
# [DESIGN] 2026 Cyberpunk UI (가독성 & 탭 크기 강화)
# ==============================================================================
st.set_page_config(page_title="2026 AI Battle Royale", layout="wide")

# 움직이는 우주 배경
bg_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHBzcDJwMXB4cTJwMXB4cTJwMXB4cTJwMXB4cTJwMXB4cTJwMXB4cTJwMXB4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/U3qYN8S0j3bpK/giphy.gif"

st.markdown(f"""
<style>
    /* 1. 배경 설정 */
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.88); /* 텍스트 가독성을 위해 어둡게 */
        z-index: -1;
    }}

    /* 2. 모든 텍스트 하얀색 강제 적용 */
    h1, h2, h3, h4, h5, h6, p, div, span, li, .stMarkdown, label {{
        color: #FFFFFF !important;
        text-shadow: 0 0 5px rgba(0,0,0,0.8);
    }}

    /* 3. 제목 스타일 */
    .title-text {{
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(0, 201, 255, 0.5);
    }}

    /* 4. 4대 천왕 카드 */
    .ai-card {{
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    .ai-card:hover {{
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.15);
        border-color: #00C9FF;
        box-shadow: 0 0 30px rgba(0, 201, 255, 0.4);
    }}
    .ai-name {{ font-size: 1.5rem; font-weight: bold; margin-bottom: 5px; }}
    .ai-desc {{ font-size: 0.9rem; color: #ddd !important; }}

    /* 5. 탭 버튼 크기 확대 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px;
        justify-content: center;
        margin-top: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 70px;
        padding: 0 30px;
        font-size: 1.5rem;
        background-color: rgba(50, 50, 50, 0.8);
        border: 2px solid #555;
        border-radius: 10px;
        color: #aaa !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #00C9FF !important;
        color: white !important;
        border-color: #00C9FF !important;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.6);
    }}

    /* 6. 요약 박스 스타일 */
    .summary-box {{
        background: rgba(20, 20, 40, 0.7);
        border: 1px solid #00C9FF;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    /* Expander 스타일 커스텀 */
    .streamlit-expanderHeader {{
        font-weight: bold;
        color: #00C9FF !important;
        background-color: rgba(255,255,255,0.05);
        border-radius: 5px;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# [DATA] 4대 AI 데이터
# ==============================================================================
models = {
    'Gemini 2.0 (Google)': [9.9, 9.7, 10.0, 9.9, 9.0, 9.5],
    'GPT-5 (OpenAI)':      [9.8, 9.9, 9.0, 9.6, 8.8, 8.5],
    'Grok 4 (xAI)':        [9.2, 9.4, 8.5, 9.0, 10.0, 8.0],
    'Claude 4 (Anthropic)':[9.9, 9.8, 9.2, 8.5, 8.5, 9.0]
}
categories = ['코딩', '추론', '문맥', '멀티모달', '속도', '에이전트']

# 투자 정보
finance_data = {
    'AI Model': ['GPT-5 (OpenAI)', 'Gemini (DeepMind)', 'Grok (xAI)', 'Claude (Anthropic)'],
    'Valuation ($B)': [250, 200, 80, 60], 
    'Backer': ['Microsoft', 'Alphabet', 'Elon Musk', 'Amazon'],
    'Investment Focus': ['초지능(AGI) / B2B', '모바일 / 에이전트', '로봇 / 물리AI', 'AI 안전 / 코딩']
}
df_finance = pd.DataFrame(finance_data)

# ==============================================================================
# [UI] 헤더 & 4대 천왕 소개
# ==============================================================================
st.markdown('<div class="title-text">🤖 2026 AI 천하제일 무술대회</div>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 40px;'>⚔️ 실리콘 왕좌의 주인은 누가 될 것인가?</h3>", unsafe_allow_html=True)

# 4대 AI 카드
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="ai-card" style="border-color: #4285F4;">
        <div style="font-size: 50px;">💎</div>
        <div class="ai-name" style="color: #4285F4 !important;">Gemini 2.0</div>
        <div class="ai-desc">"안드로이드의 지배자"<br>유니버셜 에이전트</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="ai-card" style="border-color: #10A37F;">
        <div style="font-size: 50px;">🧠</div>
        <div class="ai-name" style="color: #10A37F !important;">GPT-5 Orion</div>
        <div class="ai-desc">"추론의 절대신"<br>수학/과학 난제 해결</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="ai-card" style="border-color: #FFFFFF;">
        <div style="font-size: 50px;">🚀</div>
        <div class="ai-name" style="color: #FFFFFF !important;">Grok 4</div>
        <div class="ai-desc">"물리 세계의 정복자"<br>테슬라 로봇의 두뇌</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="ai-card" style="border-color: #D97757;">
        <div style="font-size: 50px;">💻</div>
        <div class="ai-name" style="color: #D97757 !important;">Claude 4</div>
        <div class="ai-desc">"코딩 깎는 장인"<br>개발자들의 원픽</div>
    </div>""", unsafe_allow_html=True)

st.write("") 

# ==============================================================================
# [CONTENT] 핵심 요약 (5줄) & 심층 분석 (Expander)
# ==============================================================================
st.markdown("### ⚡ 2026 전황 브리핑 (Executive Summary)")

# 5줄 핵심 요약
summary_html = """
<div class="summary-box">
    <ul style="list-style-type: none; padding: 0; font-size: 1.1rem; line-height: 1.8;">
        <li>💰 <b>[자본 전쟁]</b> 기술을 넘어 '자본력'이 승패를 가르는 10조 원 단위의 머니 게임이 시작되었습니다.</li>
        <li>📱 <b>[구글 제미나이]</b> 안드로이드 생태계를 통해 30억 명의 일상을 장악하는 '유니버셜 비서'로 진화했습니다.</li>
        <li>🏢 <b>[OpenAI GPT]</b> MS와 손잡고 기업용(B2B) 시장을 독점하며 가장 확실한 수익 모델을 구축했습니다.</li>
        <li>🤖 <b>[xAI 그록]</b> 테슬라 로봇의 물리 데이터를 학습해 현실 세계를 정복하는 가장 강력한 '다크호스'입니다.</li>
        <li>⚖️ <b>[앤스로픽 클로드]</b> '가장 안전한 AI' 포지션으로 개발자와 전문직 시장의 신뢰를 독차지하고 있습니다.</li>
    </ul>
</div>
"""
st.markdown(summary_html, unsafe_allow_html=True)

# 심층 분석 (버튼을 눌러야 나옴)
with st.expander("📂 [1급 기밀] 심층 분석 보고서 열람 (Click to Open)"):
    st.markdown("""
    #### 📜 2026 투자 & 기술 판세 심층 분석 (Analyst Report)

    **1. OpenAI (MS 연합군):** 마이크로소프트의 무한 지원을 등에 업은 OpenAI는 기업가치 **2,500억 달러(약 350조 원)**를 돌파했습니다. 이들은 막대한 자금으로 전 세계 GPU의 40%를 선점하며 '초지능(AGI)' 개발에 올인하고 있습니다. 기업용(B2B) 시장에서의 수익 모델이 가장 탄탄하여 투자자들에게 가장 매력적인 자산으로 평가받습니다.

    **2. Google DeepMind (자체 조달):** 구글은 외부 투자 없이 모회사 알파벳의 현금 보유고를 쏟아붓고 있습니다. 특히 자체 AI 반도체인 **'TPU v6'**를 개발해 엔비디아 의존도를 낮춘 것이 신의 한 수였습니다. 투자금의 대부분은 **'안드로이드 생태계 통합'**과 **'에이전트 기술'**에 집중되어, 전 세계 30억 명의 스마트폰 사용자를 락인(Lock-in) 시키는 전략을 씁니다.

    **3. xAI (머스크의 야망):** 일론 머스크의 xAI는 가장 공격적인 투자를 감행합니다. 텍사스에 건설한 세계 최대 데이터센터 **'멤피스 슈퍼클러스터'**는 그록(Grok)의 지능을 기하급수적으로 높였습니다. 투자금은 테슬라의 자율주행 및 휴머노이드 로봇(Optimus)과의 시너지를 내는 **'물리 AI'** 분야에 집중되고 있습니다.

    **4. Anthropic (반(反) MS 연합):** 마이크로소프트 진영을 견제하려는 아마존(Amazon)과 구글(Google)로부터 동시에 투자를 유치했습니다. '가장 안전한 AI'라는 브랜드 이미지를 바탕으로 금융, 의료, 법률 등 **'고신뢰 영역'**의 투자를 독식하고 있습니다.

    **결론:** 기술은 상향 평준화되었습니다. 이제는 **'누가 더 싸게(칩 효율화)', '누가 더 확실하게 돈을 버는가(수익화)'**가 관건입니다. B2B는 GPT, 모바일은 제미나이, 로봇은 그록, 전문직은 클로드가 자본을 흡수하며 시장을 4분할 하고 있습니다.
    """)

# ==============================================================================
# [TABS] 메인 차트 및 분석
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["💰 머니 게임 (Finance)", "⚔️ 스펙 레이더 (Stats)", "🔮 미래 시나리오 (Future)"])

# 1. 머니 게임
with tab1:
    c_chart, c_desc = st.columns([1.5, 1])
    with c_chart:
        st.markdown("#### 📊 기업가치(Valuation) 비교 (단위: 10억 달러)")
        fig_m, ax_m = plt.subplots(figsize=(10, 6))
        fig_m.patch.set_alpha(0.0)
        ax_m.set_facecolor('none')
        
        bars = ax_m.barh(df_finance['AI Model'], df_finance['Valuation ($B)'], 
                         color=['#10A37F', '#4285F4', '#FFFFFF', '#D97757'])
        
        for bar in bars:
            width = bar.get_width()
            ax_m.text(width + 5, bar.get_y() + bar.get_height()/2, 
                      f'${int(width)}B', va='center', color='white', fontweight='bold', fontsize=12)
            
        ax_m.spines['top'].set_visible(False)
        ax_m.spines['right'].set_visible(False)
        ax_m.spines['bottom'].set_color('white')
        ax_m.spines['left'].set_color('white')
        ax_m.tick_params(colors='white')
        st.pyplot(fig_m)

    with c_desc:
        st.markdown("#### 💼 2026 투자자 현황")
        st.dataframe(df_finance[['AI Model', 'Backer', 'Investment Focus']], hide_index=True, use_container_width=True)

# 2. 스펙 레이더
with tab2:
    col_radar, col_desc = st.columns([1.5, 1])
    with col_radar:
        fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        ax.grid(color='#555', linestyle=':', linewidth=1)
        ax.spines['polar'].set_color('#888')
        
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        
        plt.xticks(angles[:-1], categories, color='#00C9FF', size=14, fontweight='bold')
        plt.yticks([2,4,6,8,10], [], color="#333")
        plt.ylim(0, 10.5)

        colors = {'Gemini 2.0 (Google)': '#4285F4', 'GPT-5 (OpenAI)': '#10A37F', 
                  'Grok 4 (xAI)': '#FFFFFF', 'Claude 4 (Anthropic)': '#D97757'}

        for model, values in models.items():
            values += values[:1]
            ax.plot(angles, values, linewidth=3, label=model, color=colors[model])
            ax.fill(angles, values, color=colors[model], alpha=0.1)

        legend = plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), 
                            facecolor=(0,0,0,0.7), edgecolor='#555')
        plt.setp(legend.get_texts(), color='white')
        st.pyplot(fig)
        
    with col_desc:
        st.markdown("#### 📊 4대 천왕 능력치")
        st.info("💎 **제미나이:** 문맥/영상 이해 만점")
        st.info("🧠 **GPT-5:** 추론/논리 만점")
        st.info("🚀 **그록:** 속도/실시간성 만점")
        st.info("💻 **클로드:** 코딩/안전성 만점")

# 3. 미래 시나리오
with tab3:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.success("#### 🏆 제미나이 승리 시나리오")
        st.write("스마트폰 OS(안드로이드)를 가진 구글이 '개인 비서' 시장을 독점합니다. 앱스토어는 사라지고 '제미나이 스토어'의 시대가 옵니다.")
    with col_f2:
        st.warning("#### ⚠️ 그록의 로봇 혁명")
        st.write("테슬라 봇이 가정에 보급되면서 AI가 물리 세계로 나옵니다. 노동을 대체하는 그록이 가장 큰 부가가치를 창출합니다.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #aaa;'>Simulation by Gemini 2.0 | Powered by Streamlit</div>", unsafe_allow_html=True)