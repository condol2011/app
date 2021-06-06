import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('邀ｳ蝗ｽ譬ｪ萓｡蜿ｯ隕門喧繧｢繝励Μ')

st.sidebar.write("""
# GAFA譬ｪ萓｡
縺薙■繧峨�ｯ譬ｪ萓｡蜿ｯ隕門喧繝�繝ｼ繝ｫ縺ｧ縺吶ゆｻ･荳九�ｮ繧ｪ繝励す繝ｧ繝ｳ縺九ｉ陦ｨ遉ｺ譌･謨ｰ繧呈欠螳�
""")

st.sidebar.write("""
## 陦ｨ遉ｺ譌･謨ｰ驕ｸ謚�
""")

days = st.sidebar.slider('譌･謨ｰ', 1, 50, 20)

st.write(f"""
### 驕主悉 **{days}譌･髢�** 縺ｮGAFA縺ｮ譬ｪ萓｡
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
    ## 譬ｪ萓｡縺ｮ遽�蝗ｲ謖�螳�
    """)
    ymin, ymax = st.sidebar.slider(
        '遽�蝗ｲ繧呈欠螳壹＠縺ｦ縺上□縺輔＞縲�',
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
        '莨夂､ｾ蜷阪ｒ驕ｸ謚槭＠縺ｦ縺上□縺輔＞縲�',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('蟆代↑縺上→繧ゆｸ遉ｾ縺ｯ驕ｸ繧薙〒縺上□縺輔＞縲�')
    else:
        data = df.loc[companies]
        st.write('### 譬ｪ萓｡ (USD)', data.sort_index())
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
        "縺翫▲縺ｨ�ｼ√↑縺ｫ縺九お繝ｩ繝ｼ縺瑚ｵｷ縺阪※縺�繧九ｈ縺�縺ｧ縺吶�"
    )