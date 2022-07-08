import requests
import altair as alt
import pandas as pd   

url = 'https://agsi.gie.eu/api'

params = {
    "country": "de",
    "from": "2022-01-31",
    "size": 300
}

headers = {
    "x-key" : "<KEY>"
}

resp = requests.get(url=url, params=params, headers=headers)
data = resp.json()
df = pd.json_normalize(data['data'])
df['full'] = df['full'].astype(float)
df['injection'] = df['injection'].astype(float)
df['gasDayStart'] = pd.to_datetime(df['gasDayStart'], errors='coerce')
print(df)

base = alt.Chart(df).mark_line().encode(
    x = alt.X('gasDayStart', axis=alt.Axis(title="Datum", format = ("%b %Y")))
    )

line = base.mark_line(color='red').encode(y = alt.Y('full', 
    axis=alt.Axis(title ="Füllstand [%]"), scale=alt.Scale(padding=0, domain=[0,100]) ))
bar = base.mark_bar(color='green').encode(y = alt.Y('injection',
     axis=alt.Axis(title ="Einspeisung [GWh/d]") ))
    
(line+bar).properties(height=600, width=1200,  title='Gasspeicher in Deutschland' ).resolve_scale(
    y = 'independent'
).save('data.html')