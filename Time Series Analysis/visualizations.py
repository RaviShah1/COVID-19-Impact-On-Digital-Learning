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

def add_secondary_y_plot(fig: go.Figure, 
                         row: int, col: int, 
                         x1: np.array, x2: np.array, 
                         y1: np.array, y2: np.array, 
                         color1: str, color2: str,
                         name1: str, name2: str):
    fig.add_scatter(x=x1, 
                    y=y1, 
                    mode='lines',
                    marker={'color': color1},
                    name=name1,
                    secondary_y=False,
                    row=row,
                    col=col)
    
    fig.add_scatter(x=x2, 
                    y=y2, 
                    mode='lines', 
                    marker={'color': color2},
                    name=name2,
                    secondary_y=True,
                    row=row,
                    col=col)
    
def plot_engage_to_cases(engage_df: pd.DataFrame, cases_df: pd.DataFrame):
    fig =  make_subplots(rows=2, cols=1, 
                         specs=[[{'secondary_y': True}], [{'secondary_y': True}]],
                         subplot_titles=('Engagement Index VS Cumulative Cases - Over Time (US)', 'Engagement Index VS New Cases Daily - Over Time (US)'))
    add_secondary_y_plot(fig, 1, 1, engage_df.index, cases_df.index, engage_df.engagement_index, cases_df.cases, '#36B6D2', '#E76a5d', 'Engagement Index', 'COVID Cases')
    add_secondary_y_plot(fig, 2, 1, engage_df.index, cases_df.index, engage_df.engagement_index, cases_df.new_cases, '#36B6D2', '#E76a5d', 'Engagement Index', 'COVID Cases')

        
    fig.add_vline(x=dt.datetime(2020,1,21), line_width=2, line_dash='dash', line_color='#9B9B9B')
    fig.add_vline(x=dt.datetime(2020,6,1), line_width=2, line_dash='dash', line_color='#9B9B9B')
    fig.add_vline(x=dt.datetime(2020,8,12), line_width=2, line_dash='dash', line_color='#9B9B9B')

    fig.update_layout(
        autosize=False,
        width=850,
        height=450,)

    fig.update_layout(plot_bgcolor='#E6EFF1') 
    fig.update_xaxes(showgrid=False, title_text='Date')
    fig.update_yaxes(showgrid=False, title_text='Engagement Index', secondary_y=False)
    fig.update_yaxes(showgrid=False, title_text='Cases', secondary_y=True)
    fig.update_layout(title_x=.3, title_y=.92, title_font_size=30, height=750, width=1000)

    fig.show()
    
def plot_resampled_engage_to_cases(engage_df: pd.DataFrame, cases_df: pd.DataFrame):
    fig =  make_subplots(rows=3, cols=1, 
                         specs=[[{'secondary_y': True}], [{'secondary_y': True}], [{'secondary_y': True}]],
                         subplot_titles=("Daily", "Weekly", "Monthly"))
    
    add_secondary_y_plot(fig, 1, 1, engage_df.index, cases_df.index, engage_df.engagement_index, cases_df.new_cases, '#36B6D2', '#E76a5d', 'Engagement Index', 'COVID Cases')
    
    engage_df_weekly = resample(engage_df, '7D')
    cases_df_weekly = resample(cases_df, '7D', ['cases', 'new_cases'])
    add_secondary_y_plot(fig, 2, 1, engage_df_weekly.index, cases_df_weekly.index, engage_df_weekly.engagement_index, cases_df_weekly.new_cases, '#36B6D2', '#E76a5d', 'Engagement Index', 'COVID Cases')
    
    engage_df_monthly = resample(engage_df, 'M')
    cases_df_monthly = resample(cases_df, 'M', ['cases', 'new_cases'])
    add_secondary_y_plot(fig, 3, 1, engage_df_monthly.index, cases_df_monthly.index, engage_df_monthly.engagement_index, cases_df_monthly.new_cases, '#36B6D2', '#E76a5d', 'Engagement Index', 'COVID Cases')
    
    fig.add_vline(x=dt.datetime(2020,1,21), line_width=2, line_dash='dash', line_color='#9B9B9B')
    fig.add_vline(x=dt.datetime(2020,6,1), line_width=2, line_dash='dash', line_color='#9B9B9B')
    fig.add_vline(x=dt.datetime(2020,8,12), line_width=2, line_dash='dash', line_color='#9B9B9B')

    fig.update_layout(
        autosize=False,
        width=850,
        height=450,)

    fig.update_layout(plot_bgcolor='#E6EFF1') 
    fig.update_xaxes(showgrid=False, title_text='Date')
    fig.update_yaxes(showgrid=False, title_text='Engagement Index', secondary_y=False)
    fig.update_yaxes(showgrid=False, title_text='Cases', secondary_y=True)
    fig.update_layout(title_x=.3, title_y=.92, title_font_size=30, height=750, width=1000)

    fig.show()
