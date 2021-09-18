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

def plot_sample_size_details(districts_df: pd.DataFrame):
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
    fig.add_trace(
        go.Pie(labels=districts_df.state.value_counts().index, values=districts_df.state.value_counts().values, hole=.5),
        row=1, col=1)
    
    fig.add_trace(
        go.Pie(labels=districts_df.locale.value_counts().index, values=districts_df.locale.value_counts().values, hole=.5),
        row=1, col=2)
    fig.update_layout(showlegend=False)
    fig.show()
