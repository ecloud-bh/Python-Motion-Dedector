from motion_detector import df
import pandas as pd
from bokeh.plotting import figure, show, output_file


df=pd.read_csv("Kayit.csv",parse_dates=["Baslat","Bitir"])
p=figure(x_axis_type='datetime',height=100,width=500, sizing_mode='scale_width' , title="Motion Graph")

q=p.quad(left=df["Baslat"],right=df["Bitir"],bottom=0,top=1,color="green")
output_file("Graph.html")
show(p)
