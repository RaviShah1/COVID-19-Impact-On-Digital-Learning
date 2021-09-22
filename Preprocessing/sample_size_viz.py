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

long_teal = ['rgb(42, 86, 116)',
             'rgb(45, 95, 125)',
             'rgb(55, 105, 135)',
             'rgb(59, 115, 143)',
             'rgb(62, 124, 147)',
             'rgb(63, 128, 151)',
             'rgb(65, 133, 154)',
             'rgb(71, 138, 160)',
             'rgb(76, 142, 163)',
             'rgb(79, 144, 166)',
             'rgb(81, 151, 169)',
             'rgb(85, 157, 172)',
             'rgb(90, 162, 175)',
             'rgb(95, 167, 178)',
             'rgb(104, 171, 184)',
             'rgb(114, 182, 192)',
             'rgb(124, 188, 198)',
             'rgb(133, 196, 201)',
             'rgb(145, 205, 205)',
             'rgb(155, 213, 213)',
             'rgb(168, 219, 217)',
             'rgb(178, 225, 223)',
             'rgb(188, 232, 227)',
             'rgb(209, 238, 234)']
px.colors.sequential.Teal_r

def plot_sample_size_details(districts_df: pd.DataFrame, products_df: pd.DataFrame):
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
                       column_titles=['States', 'Locale', 'Product Audience'])
    fig.add_trace(
        go.Pie(labels=districts_df.state.value_counts().index, values=districts_df.state.value_counts().values, marker=dict(colors=long_teal), hole=.5, textposition='inside', textinfo='label'),
        row=1, col=1)
    
    fig.add_trace(
        go.Pie(labels=districts_df.locale.value_counts().index, values=districts_df.locale.value_counts().values, marker=dict(colors=px.colors.sequential.Teal_r), hole=.5, textposition='inside', textinfo='label'),
        row=1, col=2)
    
    fig.add_trace(
        go.Pie(labels=['Prek-12', 'Higher Ed', 'Corporate'], values=[products_df['PreK-12'].sum(), products_df['HigherEd'].sum(), products_df['Corporate'].sum()], marker=dict(colors=px.colors.sequential.Teal_r), hole=.5, textposition='inside', textinfo='label'),
        row=1, col=3)
    
    fig.update_layout(showlegend=False)
    fig.show()
