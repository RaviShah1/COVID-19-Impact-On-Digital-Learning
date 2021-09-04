import pandas as pd
import numpy as np
import glob
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", 100)

def resample(df: pd.DataFrame, sample: str, what: list=None):
    if what is not None:
        return df[what].resample(sample).mean()
    return df[['engagement_index', 'pct_access']].resample(sample).mean()
