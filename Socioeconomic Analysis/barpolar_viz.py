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

def plot_product_barpolar(df: pd.DataFrame, products_df: pd.DataFrame):
    prod_data = df.nlargest(7, 'engagement_index')
    plots = list()
    for i in range(7):
        try:
            label = str(products_df[products_df['LP ID'] == int(prod_data.index[i])]["Product Name"].values[0])
        except Exception:
            label = "not known"
        color = px.colors.sequential.Teal[6-i]
        plots.append(go.Barpolar(
            r=[prod_data.iloc[i][1]],
            theta=[(i+1)*50],
            width=[28],
            marker_color=color,
            marker_line_color="#0541a1",
            marker_line_width=2,
            name=label,
            opacity=0.8))
    fig = go.Figure(plots)

    fig.update_layout(
        template=None,
        polar = dict(
            radialaxis = dict(showticklabels=False, ticks=''),
            angularaxis = dict(showticklabels=False, ticks='')
        ),
        showlegend=True
    )

    fig.show()
