import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from sodapy import Socrata
from plots.funcio_mapa import vagueries_plot
from plots.Hist_Victor import hist1
from plots.aleix import pie_aleix

options = st.multiselect('Which years do you want to see?',['2015','2016','2017','2018','2019','2020','2021','All'],default=['All'])
# st.write('You selected:', options)
client = Socrata("analisi.transparenciacatalunya.cat", None)
if 'All' in options:
    options=['2015','2016','2017','2018','2019','2020','2021']

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get_all("pvrz-iijx") # 2000 is the number of vaccinated patients that we scrape from the web page
df=pd.DataFrame(results)
df['servei_territorial_gestio'].fillna('Altres', inplace=True)
# df['servei_territorial_gestio'].drop_duplicates()
# df.servei_territorial_gestio.value_counts()

def func(row):
    if row['servei_territorial_gestio'] in ['Barcelona ciutat']:
        return 'MB'
    elif row['servei_territorial_gestio'] in ['Àrea Metropolitana BCN']:
        return 'PE'
    elif row['servei_territorial_gestio'] in ["Terres de l'Ebre"]:
        return 'TE'
    elif row['servei_territorial_gestio'] in ["Tarragona"]:
        return 'CT'
    elif row['servei_territorial_gestio'] in ['Barcelona comarques']:
        return 'CC'
    elif row['servei_territorial_gestio'] in ['Lleida']:
        return 'PO'
    elif row['servei_territorial_gestio'] in ['Girona']:
        return 'CG'
    else:
        return 'Desconegut'


df['codi_vagueria'] = df.apply(func, axis=1)
# df['codi_vagueria'].drop_duplicates()
df2=df[df['any_entrada_sistema'].isin(options)]

#PATHFILES
df_v=list(df2['codi_vagueria'])
# df_s=(df2['sexe_infant','codi_vagueria'])
#ENTRA LA FUNCIÓ
# p = vagueries_plot(df_v)
# q,r,s = hist1(options)
ani=pie_aleix(options)
#FALTA SABER COM PASSAR UN DF COM ARGUMENT I PODER PLOTEJAR MÉS COSES
st.title("Migrants arribats a Catalunya")
st.subheader("Sel·lecció predeterminada: 2015-2021")
components.html(ani.to_jshtml(), height=2000)
# st.pyplot(q)
# st.pyplot(r)
# st.pyplot(s)
# st.bokeh_chart(p)