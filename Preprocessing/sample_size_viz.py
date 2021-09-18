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
