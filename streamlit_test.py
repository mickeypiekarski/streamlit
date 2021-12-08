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



st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

key = "266dbf914fd18fad344fcf6e0937362695777573"
nomics = Nomics(key)

img = Image.open("cryptoreview_logo.jpg")
st.title("Crypto Dashboard")
st.subheader("Mickey Piekarski, Varun Dashora, Noor Gill, Marcus Manos")

st.sidebar.image(img, width = 35)
st.sidebar.write("Send us some [feedback](https://docs.google.com/forms/d/e/1FAIpQLSeW1-wPirsWOBxF8VSJUxIGd1bM9BnT55cX5EXK6atmzAO3Hw/viewform?usp=sf_link)!")


col1, col2,col3 = st.columns((1,1,1))

# loading data







currencies_name = ['BTC', 'ETH', 'BNB', 'USDT', 'SOL', 'ADA', 'XRP', 'USDC', 'DOT', 'DOGE']
currencies  = nomics.Currencies.get_currencies(ids = 'BTC, ETH, BNB, USDT, SOL, ADA, XRP, USDC, DOT, DOGE')
currencies = pd.DataFrame(currencies)
time.sleep(1)
with col1:
    option = st.selectbox(\
    'Which coin would you like to view', currencies_name)
    'You selected: ', option

    option1 = st.selectbox(\
    'Date range (years)', [0.5,1,2,3,4,5])
    'You selected: ', option1
    coin = option
    markets = nomics.ExchangeRates.get_history(currency = coin, start = '2015-10-02T15:00:00.05Z')

    df = pd.DataFrame(markets)
    df = df.tail(int(364 * option1))
    #df.to_csv('sample_df.csv')

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date_MDY'], empty='none')


    line = alt.Chart().mark_line(interpolate='basis').encode(
    alt.X('timestamp:T', axis=alt.Axis(title='Date')),
    alt.Y('rate:Q', axis=alt.Axis(title='Price (in USD)',format='$f')),
    # color='Cryptocurrency Choice:N'
    )

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
    selectors = alt.Chart().mark_point().encode(
    x='timestamp:T',
    opacity=alt.value(0),
    ).add_selection(
    nearest
    )

# Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

# Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'rate:Q', alt.value(' '))
    )

# Draw a rule at the location of the selection
    rules = alt.Chart().mark_rule(color='gray').encode(
    x='timestamp:T',
    ).transform_filter(
    nearest
    )

    chart = alt.layer(line, selectors, points, rules, text,
                       data=df,
                       width=800, height=400,title= coin +' Price History').interactive()
    chart


    time.sleep(1)
    markets = nomics.Currencies.get_currencies(coin)
    df = pd.DataFrame(markets)
    df
with col2:
    val1 = df['price'][0]
    val2 = df['1d'][0]['price_change']
    val3 = df['market_cap'][0]
    val4 = df['1d'][0]['market_cap_change']
    st.metric("Price",smart_num(val1), smart_num(val2))
    st.metric("Market Cap", smart_num(val3),smart_num(val4))


    for i in currencies_name:
        logo = currencies[currencies['symbol']==i]
        logo = np.array(logo['logo_url'])[0]
        #st.image(logo,width = 20)




with col3:
    val1 = df['1d'][0]['volume']
    val2 = df['1d'][0]['volume_change']
    st.metric("Volume 1d",smart_num(val1),smart_num(val2))

    for i in currencies_name:
        break
        #st.write(i)
