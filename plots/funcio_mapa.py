import geopandas as gpd
import pandas_bokeh
from bokeh.palettes import Colorblind
import pandas as pd
import os
from sodapy import Socrata


def vagueries_plot(options, show_figure=False):
    client = Socrata("analisi.transparenciacatalunya.cat", None)
    if 'All' in options:
        options=['2015','2016','2017','2018','2019','2020','2021']

    results = client.get_all("pvrz-iijx")
    df=pd.DataFrame(results)
    df['servei_territorial_gestio'].fillna('Altres', inplace=True)

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
    df2=df[df['any_entrada_sistema'].isin(options)]
    #PATHFILES
    df_v=list(df2['codi_vagueria'])
    here = os.path.dirname(__file__)
    main_folder_dir = os.path.join(here, "../")
    second_folder_dir = os.path.join(here, "../capitals/")
    vagueries  = gpd.read_file(main_folder_dir+"vagueries.geojson")
    muni  = gpd.read_file(second_folder_dir+'areapoblacion_s.shp')
    muni2=muni[muni['nombre'].isin(['Barcelona','Tarragona','Girona','Lleida'])]
    muni2.rename(columns={"nombre":"Capital"}, inplace=True)
    vagueries=gpd.read_file('/home/usuario/Documentos/Master/1_AVDM/Final_Dashboard/vagueries.geojson')
    vagueries.rename(columns={"aft":"codi_vagueria",'nom_aft':'Vegueria_1'}, inplace=True)
    dw_mapping={"Metropolità de Barcelona":"Barcelona Metropolis",
               "Comarques centrals":"Central shires",
               "Penedès":"Penedès",
               "Comarques gironines":"Girona shires",
               "Alt Pirineu i Aran":"Alt Pirineu i Aran",
               "Terres de Lleida (Ponent)":"Terres de Lleida (Ponent)",
               "Camp de Tarragona":"Camp de Tarragona",
               "Terres de l'Ebre":"Terres de l'Ebre"}
    vagueries['Vegueria'] = vagueries['Vegueria_1'].map(dw_mapping)
    occurrences = [df_v.count(x) for x in df_v]
    # df_s=df[['sexe_infant','codi_vagueria']]
    # df_s2=df_s.groupby(['codi_vagueria','sexe_infant']).size().reset_index(name='counts')
    df_pre=pd.DataFrame({'codi_vagueria': df_v, 'Migrants':occurrences}).drop_duplicates()
    # pre_merge=df_s2.merge(df_pre, on=['codi_vagueria'], how='inner')
    # pre_merge.rename(columns={"sexe_infant":"Sexe"}, inplace=True)
    merge=vagueries.merge(df_pre, on=['codi_vagueria'], how='outer')
    merge['Migrants'].fillna(0,inplace=True)
    vg_map = gpd.GeoDataFrame(merge, crs=vagueries.crs)
    discr=((vg_map['codi_vagueria']=='Desconegut').any()).astype(bool)
    if discr:
        vg_map.set_index('codi_vagueria',inplace=True)
        vg_map.drop(index='Desconegut',inplace=True)
        vg_map.reset_index(inplace=True)
    mapa=vg_map.plot_bokeh(simplify_shapes=0, category="Migrants", colormap="Colorblind", legend = "Mirants settled by Vegueria", hovertool_columns=['Vegueria']+["Migrants"],show_figure=False)
    return muni2.plot_bokeh(figure=mapa,simplify_shapes=10000,legend = "Capitals",hovertool_columns=['Capital'],show_colorbar=False,show_figure=show_figure)

if __name__ == "__main__":
    """
    provide some sample input for the plot function,
    to allow for a quick preview of only this plot
    """
    options=['All']
    vagueries_plot(options, show_figure=True)
