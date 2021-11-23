import geopandas as gpd
import pandas_bokeh
from bokeh.palettes import Colorblind
import pandas as pd
import os

def vagueries_plot(df_v: list, show_figure=False):
    here = os.path.dirname(__file__)
    main_folder_dir = os.path.join(here, "../")
    second_folder_dir = os.path.join(here, "../capitals/")
    vagueries  = gpd.read_file(main_folder_dir+"vagueries.geojson")
    muni  = gpd.read_file(second_folder_dir+'areapoblacion_s.shp')
    muni2=muni[muni['nombre'].isin(['Barcelona','Tarragona','Girona','Lleida'])]
    muni2.rename(columns={"nombre":"Capital"}, inplace=True)
    vagueries=gpd.read_file('/home/usuario/Documentos/Master/1_AVDM/Final_Dashboard/vagueries.geojson')
    # vagueries.drop(columns=['id','nom_aft'], inplace=True)
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

    return muni2.plot_bokeh(figure=mapa,simplify_shapes=10000,legend = "Capitals",hovertool_columns=['Capital'],show_colorbar=False,show_figure=False)

    # return vg_map.plot_bokeh(simplify_shapes=0, category="Migrants", colormap="Colorblind", legend = "Migrants arribats per Vagueria", hovertool_columns=['Vegueria']+["Migrants"],show_figure=show_figure)
    # return vg_map.plot_bokeh(simplify_shapes=0, category="A", colormap="Spectral", legend = "Migrants arribats per Vagueria", hovertool_columns=["aft"], show_figure=show_figure)

if __name__ == "__main__":
    """
    provide some sample input for the plot function,
    to allow for a quick preview of only this plot
    """
    df_v = ['TE','CT','MB','CC','MB','CC','MB','TE','CT','PO','PO','CG']
    vagueries_plot(df_v, show_figure=True)
