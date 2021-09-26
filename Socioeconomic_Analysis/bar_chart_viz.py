import pandas as pd
import numpy as np
import glob
import datetime as dt

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.offline as po
from plotly import tools
import plotly.graph_objs as pg

import warnings
warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", 100)

def add_bar(fig: go.Figure, row: int, col: int, x: list, y: list, x_label: str):
    chart = go.Bar(x=x, y=y, marker_color=px.colors.sequential.Teal[2])
    fig.append_trace(chart, row=row, col=col)
    

def plot_socioeconomic_bar_charts(pct_black_hisp_map: dict, pct_free_lunch_map: dict):
    x = ['0.0% - 20.0%', '20.0% - 40.0%', '40.0% - 60.0%', '60.0% - 80.0%', '80.0% - 100.0%']
    y1, y2= list(), list()
    for val in x:
        y1.append(pct_black_hisp_map[val].engagement_index.mean())
        y2.append(pct_free_lunch_map[val].engagement_index.mean())
    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'bar'}, {'type':'bar'}]], 
                        column_titles=['% black & hispanic', '% free & reduced lunch'])
    add_bar(fig, 1, 1, x, y1, '%')
    add_bar(fig, 1, 2, x, y2, 'teal')
    fig.update_layout(height=400, width=1000, yaxis_title='engagement')
    fig.update_traces(showlegend=False)
    
    fig.show()
