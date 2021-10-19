import streamlit as st
import pandas as pd
from datetime import timezone
from datetime import datetime
import numpy as np
import altair as alt




st.write("lets see if my code works yala")




day_signals = pd.read_csv("ada_signals_day.csv")
hour_signals = pd.read_csv("ada_signals_hour.csv")
usd = pd.read_csv("ADA-USD.csv")
price_volume = usd[['Adj Close', 'Volume', 'Date']].rename(columns={"Adj Close" : "Price"})

# Create x-axis (time series):
# Changed label rotation for x-axis for visual ease:
base = alt.Chart(price_volume).encode(x=alt.X('Date', axis=alt.Axis(labelAngle=45)))

# Create bar for volume representation:
bar = base.mark_bar(color = 'steelblue').encode(
    # Changed color of axis labels to match datatype color:
    alt.Y('Volume', axis=alt.Axis(titleColor='steelblue')))

# Create line for price representation:
line =  base.mark_line(color='orange').encode(
    # Changed color of axis labels to match datatype color:
    alt.Y('Price', axis=alt.Axis(titleColor='orange')))

# Putting all the pieces together:
# Changed width of chart to encompass full time range for EDA:
# Changed to make interactive since size is large, but interactivity did not provide any additional insights so removed:
# Changed to add a tooltip since we are working with time series data (as mentioned in lecture):
chart = alt.layer(bar, line).resolve_scale(y='independent').encode(
        tooltip=['Date', 'Price', 'Volume']
    ).properties(width=3000, title='Cardano Price & Volume Over Time')
    # Although it does not necessarily make sense to use an interactive plot here, we decide to use the interactive line coloring feature
    # to highlight the crypto we want to focus on in Hypothesis 3
    # .interactive()

# Formatting Title:
chart.configure_title(
    fontSize=20,
    font='Times',
    color='black',
    offset=10)
