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
    html_temp = """<div class='tableauPlaceholder' id='viz1635264266252' style='position: relative'><noscript><a href='#'><img alt='2021 Daily Average Proportion of Market Value Per Crypto ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz1_16352217853570&#47;donut&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='W209TableauPrototypeViz1_16352217853570&#47;donut' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz1_16352217853570&#47;donut&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1635264266252');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
    components.html(html_temp, height= 600 )



    html_temp = """  <div class='tableauPlaceholder' id='viz1635134682510' style='position: relative'><noscript><a href='#'><img alt='2021 Average Daily Value Attributed Across Cryptos Based on Associated Reddit Signal ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz2&#47;2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='W209TableauPrototypeViz2&#47;2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz2&#47;2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1635134682510');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""

    components.html(html_temp, height = 600)


    html_temp = """<div class='tableauPlaceholder' id='viz1635135014320' style='position: relative'><noscript><a href='#'><img alt='ADA: Monthly Average Change in Open and Close Price With Size Encoded by Monthly Volume  ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz3&#47;3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='W209TableauPrototypeViz3&#47;3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;W2&#47;W209TableauPrototypeViz3&#47;3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1635135014320');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""


    components.html(html_temp, height = 600)

if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

ADA_data = pd.read_csv("ADA-USD.csv")


option = st.selectbox(\
    'Which coin do you like best?', ["ADA","BTC","ETH"])

'You selected: ', option

# EXPERIMENTING (alternative representation of price per currency)
#Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date_MDY'], empty='none')

# The basic line
line = alt.Chart().mark_line(interpolate='basis').encode(
    alt.X('Date:T', axis=alt.Axis(title='Date')),
    alt.Y('Close:Q', axis=alt.Axis(title='Price (in USD)',format='$f')),
    # color='Cryptocurrency Choice:N'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart().mark_point().encode(
    x='Date:T',
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
    text=alt.condition(nearest, 'Close:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart().mark_rule(color='gray').encode(
    x='Date:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(line, selectors, points, rules, text,
                       data=ADA_data,
                       width=800, height=400,title='Cryptocurrency Price History')


chart
