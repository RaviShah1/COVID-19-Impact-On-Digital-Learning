def resample(df: pd.DataFrame, sample: str, what: list=None):
    if what is not None:
        return df[what].resample(sample).mean()
    return df[['engagement_index', 'pct_access']].resample(sample).mean()
