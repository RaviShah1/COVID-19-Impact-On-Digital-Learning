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

def split_by_time(engage_df: pd.DataFrame, start: dt.datetime, end: dt.datetime):
    engage_df = engage_df[engage_df.index > start]
    engage_df = engage_df[engage_df.index < end]
    return engage_df.engagement_index.values

def plot_engage_box_plot(engage_df: pd.DataFrame):
    y1 = split_by_time(engage_df, dt.datetime(2019,12,31), dt.datetime(2020,1,21))
    y2 = split_by_time(engage_df, dt.datetime(2020,1,22), dt.datetime(2020,6,1))
    y3 = split_by_time(engage_df, dt.datetime(2020,6,2), dt.datetime(2020,8,12))
    y4 = split_by_time(engage_df, dt.datetime(2020,8,13), dt.datetime(2021,1,1))
    
    fig = go.Figure()
    fig.add_trace(go.Box(y=y1, marker_color=px.colors.sequential.Teal[2], name='Before COVID Hit'))
    fig.add_trace(go.Box(y=y2, marker_color=px.colors.sequential.Teal[3], name='Spring 2020'))
    fig.add_trace(go.Box(y=y3, marker_color=px.colors.sequential.Teal[1], name='Summer 2020'))
    fig.add_trace(go.Box(y=y4, marker_color=px.colors.sequential.Teal[4], name='Fall 2020'))
    fig.update_layout(height=400, width=1000, yaxis_title='engagement', title='Engagement Index Box Plots', title_x=.3) 
    fig.show()
