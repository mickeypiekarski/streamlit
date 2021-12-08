import streamlit as st
import pandas as pd
from datetime import timezone
from datetime import datetime
import numpy as np
import altair as alt
import streamlit.components.v1 as components
from PIL import Image
from nomics import Nomics
import time
import requests
from stream_helper import *
from fbprophet import Prophet
import matplotlib.pyplot as plt
from W209_final_midterm_viz import *




time.sleep(1)
#configure page_title

currencies_name = ['BTC', 'ETH', 'BNB', 'USDT', 'SOL', 'ADA', 'XRP', 'USDC', 'DOT', 'DOGE']
st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)


img = Image.open("cryptoreview_logo.jpg")
st.title("Crypto Dashboard")
st.subheader("Mickey Piekarski, Varun Dashora, Noor Gill, Marcus Manos")

st.sidebar.image(img, width = 100)
st.sidebar.write("Send us some [feedback](https://docs.google.com/forms/d/e/1FAIpQLSeW1-wPirsWOBxF8VSJUxIGd1bM9BnT55cX5EXK6atmzAO3Hw/viewform?usp=sf_link)!")

global option
option = st.sidebar.selectbox(\
'Which coin would you like to view', currencies_name)
st.sidebar.write('You selected: ', option)

global option1

option1 = st.sidebar.selectbox(\
'Date range (years)', [0.5,1,2,3,4,5])
st.sidebar.write('You selected: ', option1)


st.sidebar.markdown("""
**Goal:** Our goal is to help users understand cryptocurrency trends relating to price and media/Reddit sentiment through visualizations in order to assist in decision-making for investment portfolios.

**Intended Audience:** The intended audience is both professional and amateur cryptocurrency investors who wish to use these metrics and data to refine their portfolios. A secondary audience would be financial or economic researchers who wish to use this information to assist their analysis of the market.

**Data sources:** Cryptoreview.ai and Nomics.api
""")
#start up api
key = "266dbf914fd18fad344fcf6e0937362695777573"
nomics = Nomics(key)


coin = option
markets = nomics.ExchangeRates.get_history(currency = coin, start = '2015-10-02T15:00:00.05Z')
time.sleep(1)
df = pd.DataFrame(markets)
df = df.tail(int(364 * option1))

#df.to_csv('sample_df.csv')
#df = pd.read_csv('sample_df.csv')
df = load_data(df)
reddit = pd.read_csv('data_for_viz_project_dec052021.csv')
#df




col1, col2,col3, col4 = st.columns(4)






with col1:
    currencies  = nomics.Currencies.get_currencies(coin)
    currencies = pd.DataFrame(currencies)
    val1 = currencies['price'][0]
    val2 = currencies['1d'][0]['price_change']
    logo = np.array(currencies['logo_url'])[0]
    st.image(logo,width = 100)




with col2:
    st.metric("Price",smart_num(val1), smart_num(val2))
    val1 = currencies['1d'][0]['volume']
    val2 = currencies['1d'][0]['volume_change']
    val3 = currencies['market_cap'][0]
    val4 = currencies['1d'][0]['market_cap_change']

with col3:
    st.metric("Volume 1d",smart_num(val1),smart_num(val2))

with col4:
        st.metric("Market Cap", smart_num(val3),smart_num(val4))

st.altair_chart(candlestick_chart(df),use_container_width = True)

col1b, col2b = st.columns(2)
ra1,ra2 = rolling_avg_std(df)
with col1b:

    st.altair_chart(volatlilty_chart(df,'10-day STD:Q'),use_container_width = True)
    st.altair_chart(ra1,use_container_width = True)

    z = reddit_posts_and_price(df,reddit,coin)
    st.altair_chart(z, use_container_width = True)
with col2b:
    st.altair_chart(percent_change(df),use_container_width = True)
    st.altair_chart(ra2,use_container_width = True)
