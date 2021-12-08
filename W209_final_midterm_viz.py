# -*- coding: utf-8 -*-

# -- Sheet --

from nomics import Nomics
import pandas as pd
from datetime import timezone
from datetime import datetime
import numpy as np
import altair as alt


key = "266dbf914fd18fad344fcf6e0937362695777573"
nomics = Nomics(key)

# **Load Data**

#markets = nomics.ExchangeRates.get_history(currency = 'BTC', start = '2015-10-02T15:00:00.05Z')
#markets = pd.DataFrame(markets)
#print(markets)
#markets.to_csv('sample_df.csv')
def load_data(df):

    #load data in as csv
    #try loading in that way
    #similar to how mickey did it




    #gets the 10 day real volatlilty variance swap and classical ways, and 10-day STD
    def getvol(df, window):
        df = df.sort_values(by=['Date'], ascending=True)
        df[str(window) + '-day STD'] = df['rate'].rolling(10).std()

        df['log_rtn'] = np.log(df['rate']).diff()

        ann_factor = 365/window
        window = window
        # Var Swap (returns are not demeaned)
        df[str(window) + 'real_var'] = np.square(df['log_rtn']).rolling(window).sum() * ann_factor
        df[str(window) + 'real_vol'] = np.sqrt(df[str(window) + 'real_var'])

        # Classical (returns are demeaned, dof=1)
        df[str(window) + 'real_var'] = df['log_rtn'].rolling(window).var() * ann_factor
        df[str(window) + 'real_vol'] = np.sqrt(df[str(window) + 'real_var'])
        df = df.sort_values(by=['Date'], ascending=False)
        return df

    df['rate'] = df['rate'].astype(float)
    df['close'] = df['rate'][1:].shift(-1)
    df['Date'] = pd.to_datetime(pd.to_datetime(df['timestamp']).dt.date)
    df = getvol(df, 10)
    df = df.rename(columns={'rate': 'open'})
    df['percent_change'] = (df['open'] - df['close']) / df['close']
    df['Low'] = df.loc[:,'open':'close'].min(axis=1)
    df['High'] = df.loc[:,'open':'close'].max(axis=1)
    df = df.fillna(method="pad")
    df = df.fillna(method="bfill")


    return df



#issue with dict columns
#get from_dict columns
#add to date column to existing df
# join from_dict columns with exising df on date column
    # dicts = ['1d', '7d', '30d', '365d', 'ytd']
    # for i in dicts:
    #     new_df = df.join(pd.DataFrame.from_dict(df[i]))
    #     new_df['Date'] = df['Date']
    #     new_df['id'] = df['id']
    #     df.merge(new_df, on=['Date', 'id'])


#sample_df = load_data(markets)
#sample_df = pd.read_csv('sample_df.csv')
#print(sample_df.head())



"""
tokens = ['ADA ETH ,BTC, XRP, TRX, DOGE, LTC, BCH, VNQ, SPY']
time.sleep(1)
currencies  = nomics.Currencies.get_currencies(ids = 'ADA, ETH ,BTC, XRP, TRX, DOGE, LTC, BCH, VNQ, SPY')
currencies = pd.DataFrame(currencies)
currencies.head()


#nomics = load_data('sample_df.csv', 'btc')
#nomics.head()

# Time Series Forecasting


# **Notes**
#
# - Need to create one selector for all visualizations, figure out how to include multiple selectors in visualizations
# consider using facet to break out performance if layered/stacked charts become too common.
# - Having issue with scatterplot, once it's finished it should work better.
# - implement mean line for some value metric [link](https://altair-viz.github.io/gallery/selection_layer_bar_month.html)
# - implement comparison to other assets (Real estate, S&P etc)
#     - include volatility, price, and other metrics
# - need to make correlation matrix [link](https://github.com/altair-viz/altair/pull/1945)
# - inspiration [link](https://www.youtube.com/watch?v=XWdcpoXKRnk)
# - Visualize the number of comments vs crypto with overlay of price (size=comments)
# - add sharpe ratio, volatility (standard dev), speed (volume traded)


# **Ignore the Following Cells:**


#Creates chart with selected currency and returns from SPY in percent change
def create_comparison_with_others(df, other_df):

# input_dropdown1 = alt.binding_select(options=[None] + list(final_union_df['token'].unique()), labels=label_list)
# token_selector1 = alt.selection_single(name='Currency: ', fields=['token'], bind=input_dropdown1)
# #token_selector2 = alt.selection_single(name='x_axis', fields=['token'], bind=input_dropdown)
# brush = alt.selection(type='interval')
    brush2 = alt.selection_multi(fields=['token'])


#scales = alt.selection_interval(bind='scales')

# #select time period with this small chart
# small = alt.Chart(final_union_df).mark_bar(tooltip=True).encode(
#     x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%m/%d', labelAngle=-45), )
#     #,y=alt.Y('Date:T', axis=alt.Axis(format='%m/%y', labelAngle=-45))
#     ,color=alt.condition(brush, alt.value('red'), alt.value('grey'))
#     ).add_selection(brush).properties(width=875, height=100)

# #select multiple tokens with this small chart
    others = alt.Chart(other_df).mark_bar(tooltip=True).encode(
        x=alt.X('token:O', title=None, axis=alt.Axis(labelAngle=-45))
        ,color=alt.condition(brush2, alt.value('blue'), alt.value('grey'))
        ).add_selection(brush2).properties(width=800, height=100)


#bar height is max price for each token?

    large = alt.Chart(df).mark_line(tooltip=True).encode(
        x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%m/%d/%y', labelAngle=-45))
        ,y=alt.Y('percent_change:Q', title='Percent Change', axis=alt.Axis(format='%',  labels=True, tickSize=0))
        ,color='token'
        #alt.condition(brush, alt.value('red'), alt.value('grey'))
        ).transform_filter(brush2).properties(width=800, height=500).interactive()
# .add_selection(
#          token_selector1
#          ).transform_filter(
#              token_selector1).transform_filter(brush)




    both = alt.vconcat(others, large)
    #both = alt.vconcat(both, large)
    both.configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10,
    orient='top-right'
    )
    return both

#create_comparison_with_others()

# **Begin at this cell**


# **Needs to be fixed Chart doesn't display, might be issue with date format**

"""
def candlestick_chart(df):

    open_close_color = alt.condition("datum.open <= datum.close",
                                    alt.value("#06982d"),
                                    alt.value("#ae1325"))

    #scales = alt.selection_interval(bind='scales')


    base = alt.Chart(df).encode(
            alt.X('Date:T',
                axis=alt.Axis(
                    title='Date',
                    grid = False
                )
            ),
            color=open_close_color,
            tooltip=[alt.Tooltip('Date:T'), alt.Tooltip('open:Q', format='$'),
                    alt.Tooltip('close:Q', format='$')]
        )
        #

    rule = base.mark_rule().encode(
            alt.Y(
                'Low:Q',
                title='Price',
                scale=alt.Scale(zero=False),
            ),
            alt.Y2('High:Q')
        )

    bar = base.mark_bar().encode(
            alt.Y('open:Q'),
            alt.Y2('close:Q')
        )

    all = rule + bar
    return all.properties(title='Price of Currency over Time', width=1500, height=400).interactive()




# Prophet Time series forcasting


def get_mape(actuals, forecasts):
    MAPE = np.mean(np.abs(forecasts - actuals) / (actuals))
    return MAPE

from fbprophet import Prophet
import matplotlib.pyplot as plt


def create_forecasting_chart(df):

    #Forecasts coin data in prophet
    #takes in dataframe in form of pandas df
    #helper fcn to create_forecasting_chart
    def get_prophet_data(df):
        print(df)
        crypto_prophet = Prophet()
        experiment_df = pd.DataFrame({})
        experiment_df['ds'] = pd.to_datetime(df['timestamp']).dt.date
        experiment_df['y'] = df['close']
        train_data = experiment_df[pd.to_datetime(experiment_df['ds']) <= '2021-10-01']
        valid_data = experiment_df[pd.to_datetime(experiment_df['ds']) > '2021-10-01']
        # Fit the model on the time series.
        m_prophet = crypto_prophet.fit(train_data)
        # Create a DataFrame of future dates to create forecasts for
        future_prophet = crypto_prophet.make_future_dataframe(periods = 30)
        # Create forecast
        prophet_forecast = crypto_prophet.predict(future_prophet)
        #create data
        prophet_forecast['y'] = experiment_df['y']
        prophet_forecast['low'] = prophet_forecast.loc[:,'yhat':'y'].min(axis=1)
        prophet_forecast['high'] = prophet_forecast.loc[:,'yhat':'y'].max(axis=1)
        prophet_forecast['error'] = prophet_forecast['yhat_upper'] - prophet_forecast['yhat_lower']
        prophet_forecast['midpoint'] = prophet_forecast['low'] + abs((prophet_forecast['y'] - prophet_forecast['yhat']) / 2)
        return prophet_forecast
    prophet_forecast = get_prophet_data(df)
    difference = alt.condition("datum.yhat > datum.y",
                                      alt.value("#06982d"),
                                      alt.value("#ae1325"))
    diff2= alt.condition("datum.yhat > datum.y",
                                      alt.value("#06982d"),
                                      alt.value("#ae1325"))

    base = alt.Chart(prophet_forecast).encode(
      x=alt.X('ds:T', title='Date')

      )
    bar = base.mark_bar().encode(
      alt.Y('y:Q'),
      alt.Y2('yhat:Q'), color = difference)
    area = base.mark_area(opacity = 0.2, color='steelblue').encode(
      alt.Y('yhat_upper:Q'),
      alt.Y2('yhat_lower:Q'))

    line = base.mark_line(color='black').encode(
      alt.Y('midpoint:Q')
      )


    all = bar + area + line
    return all.properties(width=800, height=600).interactive()

"""
crypto_prophet = Prophet()

experiment_df = pd.read_csv('sample_df.csv')
experiment_df['ds'] = pd.to_datetime(experiment_df['timestamp']).dt.date
experiment_df = experiment_df.rename(columns={'rate': 'y'})
experiment_df = experiment_df.drop(columns={'Unnamed: 0', 'timestamp'})
train_data = experiment_df[pd.to_datetime(experiment_df['ds']) <= '2021-10-01']
valid_data = experiment_df[pd.to_datetime(experiment_df['ds']) > '2021-10-01']

# Fit the model on the time series.
m_prophet = crypto_prophet.fit(train_data)

# Create a DataFrame of future dates to create forecasts for.
future_prophet = crypto_prophet.make_future_dataframe(periods = 30)

# Create forecast
prophet_forecast = crypto_prophet.predict(future_prophet)


m_prophet.plot(prophet_forecast)
prophet_forecast.tail()


print('MAPE: ', get_mape(experiment_df['y'], prophet_forecast['yhat']))

prophet_forecast['y'] = experiment_df['y']
prophet_forecast['low'] = prophet_forecast.loc[:,'yhat':'y'].min(axis=1)
prophet_forecast['high'] = prophet_forecast.loc[:,'yhat':'y'].max(axis=1)
prophet_forecast['error'] = prophet_forecast['yhat_upper'] - prophet_forecast['yhat_lower']
prophet_forecast['midpoint'] = prophet_forecast['low'] + abs((prophet_forecast['y'] - prophet_forecast['yhat']) / 2)
prophet_forecast.head()

def create_forecasting_chart(prophet_forecast):

  difference = alt.condition("datum.yhat > datum.y",
                                      alt.value("#06982d"),
                                      alt.value("#ae1325"))

  diff2= alt.condition("datum.yhat > datum.y",
                                      alt.value("#06982d"),
                                      alt.value("#ae1325"))

  base = alt.Chart(prophet_forecast).encode(
      x=alt.X('ds:T', title='Date', axis=alt.Axis(format='%m/%d/%y', labelAngle=-45))

      )


  bar = base.mark_bar().encode(
      alt.Y('y:Q'),
      alt.Y2('yhat:Q'), color = difference)
  area = base.mark_area(opacity = 0.2, color='steelblue').encode(
      alt.Y('yhat_upper:Q'),
      alt.Y2('yhat_lower:Q'))

  line = base.mark_line(color='black').encode(
      alt.Y('midpoint:Q')
  )


  all = bar + area + line
  all.properties(width=800, height=600).interactive()


# **Volatlilty Chart**
#
# **Unable to display area chart with price**


sample_df.head()

#Creates chart with volatlilty overlayed with price,
#takes in dataframe with price and vol data, and
#type- string specifying the columns name with :Q


"""
def volatlilty_chart(df, vol):
    vol = alt.Chart(df).mark_line(tooltip=True).encode(
            x=alt.X('Date:T', title='Date', axis=alt.Axis( grid = False)),
            y=alt.Y(vol, title='Volatlilty', axis=alt.Axis(labels=True, tickSize=0))
            )

    price = alt.Chart(df).mark_area(opacity = 0.5, color='red').encode(
      alt.Y('open:Q', axis=alt.Axis(labelAngle=-45)))

    total = vol + price
    return total.properties(width=750, height=500).interactive()


#  #select multiple tokens with this small chart
# others = alt.Chart(nomics).mark_bar(tooltip=True).encode(
#         x=alt.X('token:O', title=None, axis=alt.Axis(labelAngle=-45))
#         ,color=alt.condition(brush2, alt.value('blue'), alt.value('grey'))
#         ).add_selection(brush2).properties(width=800, height=100)


# #bar height is max price for each token?

# large = alt.Chart(nomics).mark_line(tooltip=True).encode(
#         x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%m/%d/%y', labelAngle=-45))
#         ,y=alt.Y('10-day STD:Q', title='10 Day Volalilty', axis=alt.Axis(labels=True, tickSize=0))
#         ,color='token'
#         ).transform_filter(brush2).properties(width=800, height=500).interactive()



    # both = alt.vconcat(others, large)
    # #both = alt.vconcat(both, large)
    # both.configure_legend(
    # strokeColor='gray',
    # fillColor='#EEEEEE',
    # padding=10,
    # cornerRadius=10,
    # orient='top-right'
    # )
    # return both


#viz = volatlilty_chart(sample_df, '10-day STD:Q')


# **Needs to be fixed Chart doesn't display, might be issue with date format**


# FB prophet TS forecasting
"""

from fbprophet import Prophet
import matplotlib.pyplot as plt

crypto_prophet = Prophet()

experiment_df = pd.read_csv('sample_df.csv')
experiment_df['ds'] = pd.to_datetime(experiment_df['timestamp']).dt.date
experiment_df = experiment_df.rename(columns={'rate': 'y'})
experiment_df = experiment_df.drop(columns={'Unnamed: 0', 'timestamp'})
train_data = experiment_df[pd.to_datetime(experiment_df['ds']) <= '2021-10-01']
valid_data = experiment_df[pd.to_datetime(experiment_df['ds']) > '2021-10-01']

# Fit the model on the time series.
m_prophet = crypto_prophet.fit(train_data)

# Create a DataFrame of future dates to create forecasts for.
future_prophet = crypto_prophet.make_future_dataframe(periods = 30)

# Create forecast
prophet_forecast = crypto_prophet.predict(future_prophet)


m_prophet.plot(prophet_forecast)
prophet_forecast.tail()


print('MAPE: ', get_mape(experiment_df['y'], prophet_forecast['yhat']))

# def create_reddit_ds(df, token):
#     df = df.rename(columns={'created_utc': 'Date'})
#     df[token] = token
#     df = df.merge(final_union_df, how='left', on='Date')

# reddit_posts = pd.read_csv('reddit_posts_btc.csv')
# #reddit_posts = create_reddit_ds(reddit_posts, 'btc')
# series = str(reddit_posts['created_utc']).split()[]

sample_df.head()

#aggregate post by day
#add to final_union_df

# Get rid of non dates in date column


reddit = pd.read_csv('reddit_posts_btc.csv')
idx = reddit.index[reddit['created_utc'] == 'لباس کار']
reddit = reddit.drop(idx)
idx = reddit.index[reddit['created_utc'] == 'Need some help to understand what the issue is with F1 24TH Cheetah miners']
reddit = reddit.drop(idx)
reddit['created_utc'] = pd.to_datetime(reddit['created_utc'])
reddit['date'] = reddit['created_utc'].dt.date
reddit['hour'] = reddit['created_utc'].dt.hour
reddit_posts_granular = reddit.groupby(['date', 'hour']).agg({'title': 'count'})
reddit_posts_granular = reddit_posts_granular.reset_index()
#reddit_posts_hour = reddit.groupby(['hour']).agg({'title': 'count'})
reddit_posts_granular['prev_hour'] = reddit_posts_granular['title'].shift(1)
reddit_posts_granular['percent_change'] = (reddit_posts_granular['title'] - reddit_posts_granular['prev_hour']) / reddit_posts_granular['prev_hour']
reddit_posts_granular.head()


# **Reddit Posts Chart**


# # **Noor's Visualizations**


# Merged w/ Marcus pre-processing stuff:
# ada_df = pd.read_csv('ADA-USD.csv')
# eth_df = pd.read_csv('ETH-USD.csv')
# btc_df = pd.read_csv('BTC-USD.csv')
# xrp_df = pd.read_csv('XRP-USD.csv')
# trx_df = pd.read_csv('TRX-USD.csv')
# doge_df = pd.read_csv('DOGE-USD.csv')
# ltc_df = pd.read_csv('LTC-USD.csv')
# bch_df = pd.read_csv('BCH-USD.csv')


# ada_df['token'] = 'ADA'
# eth_df['token'] = 'ETH'
# btc_df['token'] = 'BTC'
# xrp_df['token'] = 'XRP'
# trx_df['token'] = 'TRX'
# doge_df['token'] = 'DOGE'
# ltc_df['token'] = 'LTC'
# bch_df['token'] = 'BCH'

# def pre_processing(df):
#     df['Change'] = df['Open'] - df['Adj Close']
#     df['Max Close'] = df['Close'].max()
#     df['Mean Close'] = df['Close'].mean()
#     return df

# df_list = [ada_df, eth_df, btc_df, xrp_df, trx_df, doge_df, ltc_df, bch_df]
# for df in df_list:
#     pre_processing(df)

# def concatenator(df_list):
#     union_df = pd.concat(df_list)
#     union_df['percent_change'] = (union_df['Adj Close'] - union_df['Open']) / union_df['Adj Close']
#     return union_df

# union_df = concatenator(df_list)
# union_df.head()

# Percentage change chart:

"""
def percent_change(df):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X("Date:T"),
        alt.Y("percent_change:Q", title='Percentage Change'),
        color=alt.condition("datum.percent_change < 0",
                                    alt.value("#ae1325"),
                                    alt.value("#06982d")),
        tooltip= ['Date:T', 'percent_change']
    ).properties(height=500, width=750)

    return chart.properties(title='Percentage Change of Currency Over Time', width=750, height=500).interactive()

#percent_change(sample_df)

# Rolling avg and std chart:
def rolling_avg_std(df):
    chart1 = alt.Chart(df).mark_line().encode(
        alt.X("Date:T"),
        alt.Y("close:Q", title='Close'),
        tooltip= ['Date:T', 'close:Q']
    ).properties(height=500, width=750, title='Closing Price Over Time with Moving Average')

    moving_avg = alt.Chart(df).mark_line(
        color='red',
        size=3
    ).transform_window(
        rolling_mean='mean(close)'
    ).encode(
        x='Date:T',
        y='rolling_mean:Q',
        tooltip = ['Date:T','mean(close)']
    )

    chart2 = alt.Chart(df).mark_line().encode(
        alt.X("Date:T"),
        alt.Y("close:Q", title='Close'),
        tooltip= ['Date:T', 'close:Q']
    ).properties(height=500, width=750, title='Closing Price Volatility Based on Moving Standard Deviation')

    moving_std = alt.Chart(df).mark_line(
        color='lightblue',
        size=3
    ).transform_window(
        rolling_std='stdev(close)'
    ).encode(
        x='Date:T',
        y='rolling_std:Q',
        tooltip = ['Date:T', 'rolling_std:Q']
    )

    return (chart1 + moving_avg).interactive(), (chart2 + moving_std).interactive()

"""
rolling_avg_std(sample_df)

# btc_reddit_data = pd.read_csv('reddit_posts_btc.csv')
# btc_reddit_data['mentioned?'] = btc_reddit_data.selftext.str.contains('BTC', case=True, flags=0) | btc_reddit_data.title.str.contains('BTC', case=True, flags=0)| btc_reddit_data.title.str.contains('Bitcoin', case=True, flags=0)| btc_reddit_data.selftext.str.contains('Bitcoin', case=True, flags=0)| btc_reddit_data.title.str.contains('bitcoin', case=True, flags=0)| btc_reddit_data.selftext.str.contains('bitcoin', case=True, flags=0)
# btc_reddit_data['mentioned?'] = btc_reddit_data['mentioned?'].astype(int)
# for item in btc_reddit_data['created_utc']:
#     btc_reddit_data['Date'] = datetime.strptime(item, '%m/%d/%Y %H:%M')
# # btc_reddit_data['Date'].apply(lambda x: x.strftime('%Y-%m'))
# btc_reddit_data = btc_reddit_data[: 5000]

sample_df.head()

def load_reddit_data(reddit):

    idx = reddit.index[reddit['created_utc'] == 'لباس کار']
    reddit = reddit.drop(idx)
    idx = reddit.index[reddit['created_utc'] == 'Need some help to understand what the issue is with F1 24TH Cheetah miners']
    reddit = reddit.drop(idx)
    reddit['created_utc'] = pd.to_datetime(reddit['created_utc'])
    reddit['date'] = reddit['created_utc'].dt.date
    reddit['hour'] = reddit['created_utc'].dt.hour
    reddit_posts_granular = reddit.groupby(['date']).agg({'title': 'count'})
    reddit_posts_granular = reddit_posts_granular.reset_index()
    #reddit_posts_hour = reddit.groupby(['date']).agg({'title': 'count'})
    reddit_posts_granular['prev_date'] = reddit_posts_granular['title'].shift(1)
    reddit_posts_granular['percent_change'] = (reddit_posts_granular['title'] - reddit_posts_granular['prev_date']) / reddit_posts_granular['prev_date']
    reddit_posts_granular['date'] = pd.to_datetime(reddit_posts_granular['date'])
    return reddit_posts_granular

reddit_posts_granular = load_reddit_data(pd.read_csv('reddit_posts_btc.csv'))

# Reddit Number of Posts and Currency Price Over Time:
# Create x-axis (time series):
# Changed label rotation for x-axis for visual ease:

def reddit_posts_and_price(df1, df2):
    base1 = alt.Chart(df1).encode(x=alt.X('Date:T', axis=alt.Axis(labelAngle=45)))

    bar = base1.mark_bar(color = 'lightblue').encode(
        alt.Y('close:Q'))

    base2 = alt.Chart(df2).encode(x=alt.X('date:T', axis=alt.Axis(labelAngle=45)))

    line = base2.mark_line(color = 'red').encode(
        alt.Y('title:Q'))

    chart = alt.layer(bar, line).resolve_scale(y='independent').encode(
            tooltip=['Date:T', 'Close:Q']
        )

    return chart.properties(width=3000, title='Currency Price in Relation to Number of Reddit Posts Over Time').interactive()


reddit_posts_and_price(sample_df, reddit_posts_granular)
"""




def reddit_posts_and_price(price, reddit, token):

    def load_reddit(df, token):
        red = df
        red['date'] = pd.to_datetime(red['datetime_hour']).dt.date #get the date
        red = red[red['ticker'] == token]
        red = red.groupby(by=['signal', 'date', 'ticker']).agg({'value_day': 'sum'}) #aggregate by day
        return red.filter(like='reddit_submission_num_posts', axis=0).reset_index() #filter to get submission numbers

    reddit = load_reddit(reddit, token)
    base1 = alt.Chart(price).encode(x=alt.X('Date:T', title='Date'))

    bar = base1.mark_bar(color = 'lightblue').encode(
        alt.Y('close:Q'))

    reddit['date'] = reddit['date'].astype(str)
    base2 = alt.Chart(reddit).encode(x=alt.X('date:T', title=''))

    line = base2.mark_line(color = 'red').encode(
        alt.Y('value_day:Q', title='Posts per day'))

    chart = alt.layer(bar, line).resolve_scale(y='independent').encode(
            tooltip=['Date:T', 'close:Q']
        )

    return chart.properties(width=3000, title='Currency Price in Relation to Number of Reddit Posts Over Time').interactive()
