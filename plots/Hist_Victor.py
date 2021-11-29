#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import numpy as np
import neo
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pandas_bokeh
from matplotlib.gridspec import GridSpec
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
import scipy.signal
from scipy.signal import hilbert,chirp
import scipy.io
from sodapy import Socrata


# Was not in the installation list for this course!
                          #Use "pip install sodapy" or "conda install sodapy" to install

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
def hist1(options):
    options=['All']
    client = Socrata("analisi.transparenciacatalunya.cat", None)
    if 'All' in options:
        options=['2015','2016','2017','2018','2019','2020','2021']
    print("Format of dataset: ", type(client))
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get_all("pvrz-iijx")
    df_1=pd.DataFrame(results)
    # options=['2015','2016','2017','2018','2019','2020','2021']
    df=df_1[df_1['any_entrada_sistema'].isin(options)]

    # In[9]:


    #df = pd.read_csv('Noves_arribades_d_infants_i_joves_migrats_sols_a_Catalunya.csv')
    df['data_entrada_sistema']= pd.to_datetime(df['data_entrada_sistema'])

    #columna del mes no m'agrada, faig una nova
    df['mes']= df['data_entrada_sistema'].dt.month


    df['day_of_week'] = df['data_entrada_sistema'].dt.dayofweek

    df['any_entrada']= df['data_entrada_sistema'].dt.year

    # In[10]:


    dw_mapping={
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    df['day_of_week_name']=df['data_entrada_sistema'].dt.weekday.map(dw_mapping)


    df['data_naixement_infant']= pd.to_datetime(df['data_naixement_infant'])
    df['any_naixement']= df['data_naixement_infant'].dt.year
    df['Edat_arribada'] = df["any_entrada"]-df["any_naixement"]
    dw_mapping={"Africa subsahariana":"Sub-Saharan Africa",
               "Marroc":"Morroco",
               "Magreb (excloent Marroc)":"Maghreb",
               "Altra":"Others"}
    df['origen'] = df['origen_infant'].map(dw_mapping)

    pandas_bokeh.output_file('INTENTO')
    # # df.hist(column='Edat_arribada',by='sexe_infant',sharex=True,sharey=True)
    colors = ['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7']
    sns.set_palette(sns.color_palette(colors))
    rcParams['font.family'] = 'serif'

    df2 = df.groupby(['Edat_arribada', 'origen'])['Edat_arribada'].count().unstack('origen').fillna(0)
    # chicas = df[df['sexe_infant']=='Noies']
    # df2 = chicas.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    plt.tight_layout()
    fig=df2.plot_bokeh(kind='bar', stacked=True,legend=True,xticks=np.arange(0,36,3),xlabel='Arrival age',ylabel='Number of people',show_figure=False)

<<<<<<< HEAD
    return fig
=======
    # plt.title(' _   ')

    # df2 = df.groupby(['Edat_arribada', 'origen_infant'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    # fig,ax=plt.subplots()
    # df2.plot(ax=ax,kind='bar', stacked=True,color=colors)
    # plt.xlabel("Edat d'arribada")
    # plt.ylabel('Numero de persones')
    # plt.tight_layout()
    # plt.legend(loc='upper left',fontsize='9')
    # # plt.show(fig)
    #
    # chicos = df[df['sexe_infant']=='Nois']
    # df2 = chicos.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    # fig2,ax2=plt.subplots()
    # df2.plot(ax=ax2,kind='bar', stacked=True,color=colors)
    # plt.xlabel("Edat d'arribada")
    # plt.ylabel('Numero de nois')
    # plt.tight_layout()
    # plt.legend(loc='upper left',fontsize='9')
    # # plt.show(fig2)
    #
    # chicas = df[df['sexe_infant']=='Noies']
    # df2 = chicas.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    # fig3,ax3=plt.subplots()
    # df2.plot(ax=ax3,kind='bar', stacked=True,color=colors)
    # plt.xlabel("Edat d'arribada")
    # plt.ylabel('Numero de noies')
    # plt.tight_layout()
    # plt.legend(loc='upper left',fontsize='9')
    # plt.show()
    return fig
    # ,fig2,fig3
>>>>>>> 95ebc2da40916da5c23ef481433d5dd7e4c78eb0

if __name__ == "__main__":
    """
    provide some sample input for the plot function,
    to allow for a quick preview of only this plot
    """
    options=['All']
    fig=hist1(options)
    plt.show()
