import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from plots.funcio_mapa import vagueries_plot
from plots.Hist_Victor import hist1
from plots.aleix import pie_aleix

options = st.multiselect('Which years do you want to see?',['2015','2016','2017','2018','2019','2020','2021','All'],default=['All'])










p = vagueries_plot(options)
q= hist1(options)
ani=pie_aleix(options)
#FALTA SABER COM PASSAR UN DF COM ARGUMENT I PODER PLOTEJAR MÉS COSES
st.title("Migrants arribats a Catalunya")
st.write("Sel·lecció predeterminada: 2015-2021")
st.bokeh_chart(q)
st.caption("Caption1")
st.bokeh_chart(p)
st.caption("Caption2")
st.subheader("Subheader")

components.html(ani.to_jshtml(), height=1000)
