import streamlit as st
import pandas as pd
from datetime import timezone
from datetime import datetime
import numpy as np
import altair as alt
import streamlit.components.v1 as components


#testing to bring in the data


day_signals = pd.read_csv("ada_signals_day.csv")
hour_signals = pd.read_csv("ada_signals_hour.csv")
usd = pd.read_csv("ADA-USD.csv")
day_signals = pd.read_csv("data_for_viz_project.csv")



def main():
    html_temp = """<div class='tableauPlaceholder' id='viz1635134207310' style='position: relative'><noscript><a href='#'><img alt='2021 Daily Average Proportion of Market Value Per Crypto ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz1&#47;1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='W209TableauPrototypeViz1&#47;1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz1&#47;1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1635134207310');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='80%';vizElement.style.height=(divElement.offsetWidth*0.5)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
    components.html(html_temp, height= 600 )



    html_temp = """  <div class='tableauPlaceholder' id='viz1635134682510' style='position: relative'><noscript><a href='#'><img alt='2021 Average Daily Value Attributed Across Cryptos Based on Associated Reddit Signal ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz2&#47;2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='W209TableauPrototypeViz2&#47;2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz2&#47;2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1635134682510');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""

    components.html(html_temp, height = 600)


    html_temp = """<div class='tableauPlaceholder' id='viz1635135014320' style='position: relative'><noscript><a href='#'><img alt='ADA: Monthly Average Change in Open and Close Price With Size Encoded by Monthly Volume  ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz3&#47;3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='W209TableauPrototypeViz3&#47;3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz3&#47;3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1635135014320');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""


    components.html(html_temp, height = 600)

if __name__ == "__main__":
    main()



day_signals['date'] = pd.to_datetime(day_signals['datetime_hour'])

day_signals_trunc = day_signals
day_signals_trunc['date_MDY'] = pd.to_datetime(day_signals_trunc['date']).apply(lambda x: x.strftime("%m-%d-%Y"))
column_sel = ['ticker', 'value_day', 'date_MDY']

day_signals_trunc = day_signals_trunc.groupby(['date_MDY', 'ticker']).agg('mean')
day_signals_trunc = day_signals_trunc.reset_index()
day_signals_trunc = day_signals_trunc[day_signals_trunc['date_MDY'] != '12-31-2020']


day_signals_trunc = day_signals_trunc.rename(columns={'ticker' : 'Cryptocurrency Choice'})
day_signals_trunc = day_signals_trunc.rename(columns={'value_day' : 'Value'})

selection = alt.selection_multi(fields=['Cryptocurrency Choice'], name='Crypto Choice')
color = alt.condition(selection,
                      alt.Color('Cryptocurrency Choice:N', legend=None),
                      alt.value('lightgray'))

chart = alt.Chart(day_signals_trunc).mark_bar().encode(
    x=alt.X('date_MDY', title='Date'),
    y=alt.Y('Value', axis=alt.Axis(title='Value (in USD)',format='$f')),
    color=color, tooltip = ['Cryptocurrency Choice', 'Value']
).properties(title='Price of Various Cryptocurrencies Over Course of Year').add_selection(
    selection
)

legend = alt.Chart(day_signals_trunc).mark_point().encode(
    y=alt.Y('Cryptocurrency Choice:N', axis=alt.Axis(orient='right')),
    color=color
).add_selection(
    selection
)

(chart | legend)
