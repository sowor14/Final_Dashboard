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
    client = Socrata("analisi.transparenciacatalunya.cat", None)
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


    # # df.hist(column='Edat_arribada',by='sexe_infant',sharex=True,sharey=True)
    colors = ['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7']
    sns.set_palette(sns.color_palette(colors))
    rcParams['font.family'] = 'serif'

    df2 = df.groupby(['Edat_arribada', 'origen_infant'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    fig,ax=plt.subplots()
    df2.plot(ax=ax,kind='bar', stacked=True,color=colors)
    plt.xlabel("Edat d'arribada")
    plt.ylabel('Numero de persones')
    plt.tight_layout()
    plt.legend(loc='upper left',fontsize='9')
    # plt.show(fig)

    chicos = df[df['sexe_infant']=='Nois']
    df2 = chicos.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    fig2,ax2=plt.subplots()
    df2.plot(ax=ax2,kind='bar', stacked=True,color=colors)
    plt.xlabel("Edat d'arribada")
    plt.ylabel('Numero de nois')
    plt.tight_layout()
    plt.legend(loc='upper left',fontsize='9')
    # plt.show(fig2)

    chicas = df[df['sexe_infant']=='Noies']
    df2 = chicas.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
    fig3,ax3=plt.subplots()
    df2.plot(ax=ax3,kind='bar', stacked=True,color=colors)
    plt.xlabel("Edat d'arribada")
    plt.ylabel('Numero de noies')
    plt.tight_layout()
    plt.legend(loc='upper left',fontsize='9')
    # plt.show()
    return fig,fig2,fig3

if __name__ == "__main__":
    """
    provide some sample input for the plot function,
    to allow for a quick preview of only this plot
    """
    options=['2015','2016','2017','2018','2019','2020','2021']
    fig,fig2,fig3=hist1(options)
    plt.show()


#CREO UN HISTOGRAMA CON EL NUMERO DE CHICAS/CHICOS EN FUNCION DE LA EDAD CON
#LA QUE LLEGARON A CATALUNA COMPARADOS EN PARALELO. |_| |_|.

# fig=plt.figure()
# ax0=plt.subplot(222)
# plt.xlabel('Edat')
# plt.ylabel('Persones')
# plt.tight_layout()

# ax1=plt.subplot(221)
# plt.xlabel('Edat')
# plt.ylabel('Persones')
# plt.tight_layout()

# df.hist(column='Edat_arribada',by='sexe_infant',sharex=True,sharey=True,ax=(ax0,ax1),color=colors[6])
# plt.tight_layout()
# plt.show()


# #CREA EL HISTO DE SOLO LOS CHICOS

# edat_arribada=df[['Edat_arribada','sexe_infant']]
# nomes_nois=edat_arribada[edat_arribada['sexe_infant']=='Nois']
# Nois=nomes_nois['Edat_arribada']
# ax=Nois.plot.hist(bins=24, alpha=0.5,label='Nois',color=colors[0])
# plt.xlabel('Edat')
# plt.ylabel('Persones')
# plt.legend()
# plt.show()

# #CREA EL HISTO DE SOLO LAS CHICAS
# nomes_noies=edat_arribada[edat_arribada['sexe_infant']=='Noies']
# Noies=nomes_noies['Edat_arribada']
# ax=Noies.plot.hist(bins=12, alpha=0.5,label='Noies',color=colors[1])
# plt.xlabel('Edat')
# plt.ylabel('Persones')
# plt.legend()
# plt.show()


# # ###############################################################################
# #CREA EL HISTO DE LAS PERSONAS (CHICOS+CHICAS) QUE LLEGARON EN LOS DIFRENTES AÑOS
# #COMPARADOS EN PARALELO

# fig=plt.figure()
# ax0=plt.subplot(222)
# plt.xlabel('Any entrada')
# plt.ylabel('Persones')
# plt.tight_layout()

# ax1=plt.subplot(221)
# plt.xlabel('Any entrada')
# plt.ylabel('Persones')
# plt.tight_layout()

# df.hist(column='any_entrada',bins=7,by='sexe_infant',sharex=True,sharey=True,ax=(ax0,ax1),color=colors[4])
# plt.tight_layout()
# plt.show()

# #CREA EL HISTO DE LOS CHICOS QUE LLEGARON EN LOS DIFRENTES AÑOS

# any_entrada_sist=df[['any_entrada','sexe_infant']]
# nomes_nois_arribada=any_entrada_sist[any_entrada_sist['sexe_infant']=='Nois']
# Nois_arribada=nomes_nois_arribada['any_entrada']
# ax=Nois_arribada.plot.hist(bins=7, alpha=0.5,label='Nois',color=colors[2])
# plt.xlabel('Any arribada')
# plt.ylabel('Persones')
# plt.legend()
# plt.show()

# #CREA EL HISTO DE LOS CHICAS QUE LLEGARON EN LOS DIFRENTES AÑOS

# nomes_noies_arribada=any_entrada_sist[any_entrada_sist['sexe_infant']=='Noies']
# Noies_arribada=nomes_noies_arribada['any_entrada']
# ax=Noies_arribada.plot.hist(bins=7, alpha=0.5,label='Noies',color=colors[3])
# plt.xlabel('Any arribada')
# plt.ylabel('Persones')
# plt.legend()
# plt.show()

# #############################################################################
# # CREA EL HISTO  DE LAS PERSONAS EN FUNCION DEL PAIS DE ORIGEN
# # EN PARALELO CHICOS-CHICAS

# fig=plt.figure()
# ax0=plt.subplot(222)
# plt.ylabel('Persones')
# # plt.tight_layout()

# ax1=plt.subplot(221)
# plt.ylabel('Persones')
# plt.tight_layout()

# df.hist(column='origen_infant',bins=4,by='sexe_infant',sharex=True,sharey=True,ax=(ax0,ax1),color=colors[4],rot=70)
# plt.tight_layout()
# plt.show()


# # Crea el histo de personas totales
# origen_sexe=df[['origen_infant','sexe_infant']]
# nomes_nois_origen=origen_sexe[origen_sexe['sexe_infant']=='Nois']
# Nois_origen=nomes_nois_origen['origen_infant']
# pd.Series(Nois_origen).value_counts().plot(kind='bar',rot=45)
# plt.ylabel('Numero de persones')
# plt.show()

# nomes_noies_origen=origen_sexe[origen_sexe['sexe_infant']=='Noies']
# Noies_origen=nomes_noies_origen['origen_infant']
# pd.Series(Noies_origen).value_counts().plot(kind='bar',rot=45)
# plt.ylabel('Numero de persones')
# plt.show()

# #############################################################################
##HISTOGRAMA DE LA GENTE POR AÑO Y DENTRO DE LAS BARRAS POR PAIS

# df2 = df.groupby(['origen_infant', 'any_entrada'])['any_entrada'].count().unstack('origen_infant').fillna(0)
# ax=df2.plot(kind='bar', stacked=True,color=colors)
# plt.xlabel("Any d'entrada")
# plt.ylabel('Numero de persones')
# plt.tight_layout()
# plt.legend(loc='upper left',fontsize='9')
# plt.show()

# # SOLO CHICOS
# chicos = df[df['sexe_infant']=='Nois']
# df2 = chicos.groupby(['origen_infant', 'any_entrada'])['any_entrada'].count().unstack('origen_infant').fillna(0)
# ax=df2.plot(kind='bar', stacked=True,color=colors)
# plt.ylabel('Numero de nois')
# plt.xlabel("Any d'entrada")
# plt.tight_layout()
# plt.legend(loc='upper left',fontsize='9')
# plt.show()

# # SOLO CHICAS
# chicas = df[df['sexe_infant']=='Noies']
# df2 = chicas.groupby(['origen_infant', 'any_entrada'])['any_entrada'].count().unstack('origen_infant').fillna(0)
# ax=df2.plot(kind='bar', stacked=True,color=colors)
# plt.ylabel('Numero de noies')
# plt.xlabel("Any d'entrada")
# plt.tight_layout()
# plt.legend(loc='upper left',fontsize='9')
# plt.show()


# #############################################################################
##HISTOGRAMA DE LA GENTE POR EDAD Y DENTRO DE LAS BARRAS POR PAIS



# chicos = df[df['sexe_infant']=='Nois']
# df2 = chicos.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
# ax=df2.plot(kind='bar', stacked=True,color=colors)
# plt.xlabel("Edat d'arribada")
# plt.ylabel('Numero de nois')
# plt.tight_layout()
# plt.legend(loc='upper left',fontsize='9')
# plt.show()
#
# chicas = df[df['sexe_infant']=='Noies']
# df2 = chicas.groupby(['origen_infant', 'Edat_arribada'])['Edat_arribada'].count().unstack('origen_infant').fillna(0)
# ax=df2.plot(kind='bar', stacked=True,color=colors)
# plt.xlabel("Edat d'arribada")
# plt.ylabel('Numero de noies')
# plt.tight_layout()
# plt.legend(loc='upper left',fontsize='9')
# plt.show()
