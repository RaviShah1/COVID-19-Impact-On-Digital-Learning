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

def add_map(fig: go.Figure, row: int, col: int, color: str, vals: list):
    fig.add_trace(
        go.Choropleth(
            locations=st_ids,
            locationmode = 'USA-states',
            z = vals,
            colorscale=color, 
        ),
        row=row, col=col
    )
    
def segment_data_by_time(state_map: dict, df_type: int, start_date: dt.datetime, end_date: dt.datetime):
    vals = list()
    for st in list(state_map.keys()):
        df = state_map[st][df_type][state_map[st][df_type].index < end_date]
        df = df[df.index > start_date]
        if(df_type==0):
            if(len(df)>0):
                vals.append(df['new_cases'].mean())
        else:
            vals.append(df['engagement_index'].mean())
            
    return vals

def plot_engage_cases_maps_over_time(state_map: dict):
    rows = 4
    cols = 2
    fig = make_subplots(rows=4, cols=2, 
                        column_titles=['Engagement', 'Cases'], 
                        row_titles=['Before COVID Hit', 'Spring 2020', 'Summer 2020', 'Fall 2020'],
                        specs=[[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)])


    add_map(fig, 1,1,'teal', segment_data_by_time(state_map, 1, dt.datetime(2019,12,31), dt.datetime(2020,1,21)))
    add_map(fig, 2,1,'teal', segment_data_by_time(state_map, 1, dt.datetime(2020,1,22), dt.datetime(2020,6,1)))
    add_map(fig, 3,1,'teal', segment_data_by_time(state_map, 1, dt.datetime(2020,6,2), dt.datetime(2020,8,12)))
    add_map(fig, 4,1,'teal', segment_data_by_time(state_map, 1, dt.datetime(2020,8,13), dt.datetime(2021,1,1)))

    add_map(fig, 1,2,'orrd', segment_data_by_time(state_map, 0, dt.datetime(2019,12,31), dt.datetime(2020,1,21)))
    add_map(fig, 2,2,'orrd', segment_data_by_time(state_map, 0, dt.datetime(2020,1,22), dt.datetime(2020,6,1)))
    add_map(fig, 3,2,'orrd', segment_data_by_time(state_map, 0, dt.datetime(2020,6,2), dt.datetime(2020,8,12)))
    add_map(fig, 4,2,'orrd', segment_data_by_time(state_map, 0, dt.datetime(2020,8,13), dt.datetime(2021,1,1)))

    layout = dict(geo = dict(scope='usa'), height=1000, width=1000, title_font_size=30)
    fig.update_traces(showscale=False)
    fig.update_layout(layout)
    fig.update_geos(scope='usa')

    fig.show()
