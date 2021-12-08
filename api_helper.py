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
from stream_helper import smart_num





key = "266dbf914fd18fad344fcf6e0937362695777573"
nomics = Nomics(key)
markets = nomics.ExchangeRates.get_history(currency = coin, start = '2015-10-02T15:00:00.05Z')
df = pd.DataFrame(markets)
