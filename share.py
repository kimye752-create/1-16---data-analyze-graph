import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np 
import os # 파일 경로 확인용
import platform # 운영체제 확인용 (폰트 설정)

# -----------------------------------------------------------------------------
# [한글 폰트 설정] 그래프 깨짐 방지용 코드
if platform.system() == 'Darwin': # 맥
    plt.rc('font', family='AppleGothic') 
elif platform.system() == 'Windows': # 윈도우
    plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False 
# -----------------------------------------------------------------------------

st.title("💸💰국세청 근로소득 데이터 분석기")

# 다운로드 받은 데이터 불러오기 

# (변수명)
# file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"
# 데이터 파일과 내가 실행작업하는 파일과 같은 레벨에 있을 때.
# 
# 그러나 상위 급의 다른 폴더에 있을 땐 
# (변수명 파일패스) : 데이터 파일 명이 너무 길어서 변수로 이름 변경함.
# file_path = "./data/파일명을 적으면 됨.
#          ./ -> 현재의 위치에서 이 파일을 찾아와.  
#          반대로
#          ../ 는 내가 지금 작업하는 파일보다 상위레벨에 있는 데이터 파일을 참조할 때 사용.
# 경로가 중요!!!!!!

file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

# 혹시나 오류가 있을 때 를 대비해 try-except 문 사용 / 엑셀의 if error문과 유사.
try: # 오류가 없을 때 이걸 출력해.
    
    ########## 자료 읽기      #df로 파일 이름 가져오는 것임.
    # [수정됨] utf-8 오류 해결을 위해 cp949로 변경
    df = pd.read_csv(file_path, encoding='cp949') # df 라는 변수를 잡아줘야 파일이 안날라다님.
    st.success("파일이 성공적으로 불러와졌습니다!")

    ########## 데이터 미리 보기
    st.subheader("😊데이터 미리 보기")  # 제목
    st.dataframe(df.head())  # st.dataframe() : 스트림릿에서 데이터프레임을 보여주는 함수
                             # 전체 데이터가 아니라 일부 데이터만 보여주는 .head() 메소드.
                             # 기본 5개 / 10개 넣고 싶으면 .head(10)

    ######### 데이터 분석 그래프 그리기
    st.subheader("📊항목별 분포 그래프")

    ######### 분석하고 싶은 열 이름 선택
    # 예를 들어 급여나 인원 같은 숫자 데이터가 있는 열을 골라야 한다.

    column_names = df.columns.tolist()  # 데이터프레임의 열 이름을 리스트로 변환
                                        # 맨 위 항목을 제목으로 이 열을 가져올게.
    
    selected_column = st.selectbox("분석할 항목을 선택하세요", column_names)
    # 하향모양 버튼 눌르면 선택지가 좌르륵 펼쳐지고 하나 선택하는 라벨

    # 항목이 선택되었을 때만 그래프 그리기
    if selected_column:
        # 그래프 그리기 seaborn 사용
        fig, ax = plt.subplots(figsize=(10, 5))  # 새로운 그래프 그릴 준비
                    # figsize는 그래프의 크기. 그래프 그릴 도화지 크기라고 생각하면 됨.
                    # fig는 도화지, ax는 실제 그래프 그릴 부분.

        # matplotlib , seaborn 중 seaborn이 더 그래프 잘 그림. 엑셀이 가장 좋음.  / # 6문 뒤에 숫자는 투명도
        # dropna()로 빈 값 제거 후 그림
        sns.histplot(df[selected_column].dropna(), kde=True, ax=ax, color="#cc00ff50") # 막대 그래프

        plt.title(f"[{selected_column}] 분포 확인") # 그래프 맨 위 제목
        plt.xlabel(selected_column)  # x축 라벨 / 예: 급여액
        plt.ylabel("빈도수")          # y축 라벨 / 예: 빈도수

        ###### 스트림릿에 그래프 출력
        st.pyplot(fig) 

except FileNotFoundError:
    st.error(f"🚨'{file_path}'파일을 찾을 수 없습니다. 파일명을 재확인 해주세요.")
    st.stop()
except UnicodeDecodeError:
    st.error("🚨인코딩 오류가 발생했습니다. encoding='cp949' 로 설정되어 있는지 확인하세요.")
except Exception as e:
    st.error(f"🚨파일을 불러오는 중 에러가 발생했습니다: {e}")
