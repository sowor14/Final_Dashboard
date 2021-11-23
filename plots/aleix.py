# %% codecell
#Roger Bellido Peralta
#15/11/2021
#Dashboard

import pandas as pd
import streamlit as st
from sodapy import Socrata # Was not in the installation list for this course!
                           #Use "pip install sodapy" or "conda install sodapy" to install
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def pie_aleix(options):
    client = Socrata("analisi.transparenciacatalunya.cat", None)
    print("Format of dataset: ", type(client))

    results = client.get_all("pvrz-iijx") # 2000 is the number of vaccinated patients that we scrape from the web page
    df_1=pd.DataFrame(results)
    options=['2015','2016','2017','2018','2019','2020','2021']
    df=df_1[df_1['any_entrada_sistema'].isin(options)]

    df= df.sort_values("data_entrada_sistema")
    rcParams['font.family'] = 'serif'
    colors = ['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7']
    year = ["2016","2017","2018","2019","2020","2021"]
    origen_total = df["origen_infant"].value_counts().tolist()
    labels_total = df["origen_infant"].value_counts().index
    exp= [0.01,0.01,0.01,0.01]

    #plt.pie(origen_total,labels=labels_total, textprops ={"fontweight":"bold","size":15},
    #         autopct="%1.1f%%",colors = colors, shadow= True,explode = exp,startangle=180,pctdistance = 0.7,radius=2)
    # plt.pie(origen_total, colors = ["white"])
    # plt.show()
    # %% codecell
    colors_dict={ 'Marroc':"#E69F00",'Magreb (excloent Marroc)':'#56B4E9',
                 'Africa subsahariana':'#009E73','Altra':'#F0E442'}

    # f, ax = plt.subplots(figsize=(7,7))
    # df_any= df[df["any_entrada_sistema"]==year[5]]
    # origen_any = df_any["origen_infant"].value_counts()#.tolist()
    # labels_any = df_any["origen_infant"].value_counts().index
    # list_countries = list(colors_dict.keys())
    # #print(origen_any)
    # origen_any =origen_any.reindex(list_countries)
    # cdict = {"Marroc":'#E69F00',"Altra":"#56B4E9","Africa subsahariana"'#009E73'
    #         "Magreb (excloent Marroc)":'#F0E442'}
    # exp= [0.01,0.01,0.01,0.01]

    #colors2=[colors_dict[x] for x in origen_any.index]
    # origen_any.plot.pie( textprops ={"fontweight":"bold","size":15}, autopct="%1.1f%%",colors = colors, shadow= True,explode = exp,pctdistance = 0.7,radius=3,startangle=180)
    # #plt.pie(origen_any,labels=labels_any, textprops ={"fontweight":"bold","size":15},
    # #        autopct="%1.1f%%",colors = colors, shadow= True,explode = exp,pctdistance = 0.7,radius=2)
    # plt.pie(origen_total, colors = ["white"])
    # #centre_circle = plt.Circle((-5,0),70,fc= "white")
    # plt.gca().axis("equal")
    #
    # plt.title("Origen Migratori",loc="left",size=15)
    # ax.set_axis_off()
    # plt.show()
    # %% codecell
    pie_1, ax = plt.subplots(figsize=(7,7))
    colors_dict={ 'Marroc':"#E69F00",'Magreb (excloent Marroc)':'#56B4E9',
                 'Africa subsahariana':'#009E73','Altra':'#F0E442'}
    year = ["2016","2017","2018","2019","2020","2021"]
    frames = len(year)
    def animation_pie(i):
        ax.clear()
        df_any= df[df["any_entrada_sistema"]==year[i]]
        origen_any = df_any["origen_infant"].value_counts()#.tolist()
        labels_any = df_any["origen_infant"].value_counts().index
        list_countries = list(colors_dict.keys())
        origen_any =origen_any.reindex(list_countries)
        exp= [0.01,0.01,0.01,0.01]

        line_pie =origen_any.plot.pie(ax=ax,textprops ={"fontweight":"bold","size":15}, autopct="%1.1f%%",colors = colors, shadow= True,explode = exp,pctdistance = 0.7,radius=2,startangle=180)

        plt.pie(origen_total, colors = ["white"])
        plt.gca().axis("equal")

        plt.title("Migratory Origin\n"+year[i],loc="left",size=15)
        ax.set_axis_off()
        return line_pie


    ani = animation.FuncAnimation(fig = pie_1,func =animation_pie,frames =frames,interval = 500)

    return ani

if __name__ == "__main__":
    """
    provide some sample input for the plot function,
    to allow for a quick preview of only this plot
    """
    options=['2015','2016','2017','2018','2019','2020','2021']
    ani=pie_aleix(options)
    plt.show()
