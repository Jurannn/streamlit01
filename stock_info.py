import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import openpyxl


st.markdown('# 무슨 주식을 사야 부자가 되려나...')
with st.sidebar:
    st.write('## 회사 이름과 기간을 입력하세요')
    stock_name = st.text_input("회사이름")
    dr = st.date_input("시작일 - 종료일", (datetime.date(2019, 1, 1), datetime.date(2021, 12, 31)))
    st.sidebar.button('주가 데이터 확인')

@st.cache_data
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
    method = "download"
    url = "{0}?method={1}".format(base_url, method)   
    df = pd.read_html(url, header=0, encoding = 'euc-kr')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
    #df = df[['회사명','종목코드']]
    return df

def get_ticker_symbol(company_name):     
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values
    if len(code) > 0:
        ticker_symbol = code[0]
    elif (company_name != '') & (len(code) == 0):
        ticker_symbol = None  # Handle case where company name is not found
        st.write(f"### {company_name} : 해당 종목이 존재하지 않습니다.")
    if company_name == '':  # Handle case where company name is not found
        ticker_symbol = None
        st.write(f"### 종목 코드를 입력해 주세요.")
    return ticker_symbol

x = get_ticker_symbol(stock_name)

if bool(x):
    price_df = fdr.DataReader(x, dr[0], dr[1])


    st.write(f'### [{stock_name}] 주가데이터')
    st.write(price_df.head())

    price_df = price_df.reset_index()
    st.write(px.line(x = price_df['Date'], y = price_df['Close'], labels= {'x':'날짜', 'y':f'{stock_name}의 종가'}))


    col1, col2 = st.columns(2)
    col1.download_button(
        label="CSV 파일 다운로드",
        data=price_df.to_csv(),
        file_name='stock_data.csv'
    )

    excel_file = BytesIO()
    price_df.to_excel(excel_file, index=False, sheet_name='Stock Data')
    excel_file.seek(0)
    col2.download_button(
        label="엑셀 파일 다운로드",
        data=excel_file,
        file_name='stock_data.xlsx')
