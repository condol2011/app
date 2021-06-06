import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('�č����������A�v��')

st.sidebar.write("""
# GAFA����
������͊��������c�[���ł��B�ȉ��̃I�v�V��������\���������w��
""")

st.sidebar.write("""
## �\�������I��
""")

days = st.sidebar.slider('����', 1, 50, 20)

st.write(f"""
### �ߋ� **{days}����** ��GAFA����
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## �����͈͎̔w��
    """)
    ymin, ymax = st.sidebar.slider(
        '�͈͂��w�肵�Ă��������B',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        '��Ɩ���I�����Ă��������B',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('���Ȃ��Ƃ���Ђ͑I��ł��������B')
    else:
        data = df.loc[companies]
        st.write('### ���� (USD)', data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
        columns={'value': 'Stock Prices(USD)'}
        )

        chart= (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "�����ƁI�Ȃɂ��G���[���N���Ă���悤�ł��B"
    )