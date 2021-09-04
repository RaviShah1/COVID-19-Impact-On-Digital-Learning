""" 
The original data/input for all these functions can be located at the following sources:
1) https://www.kaggle.com/c/learnplatform-covid19-impact-on-digital-learning/data
2) https://github.com/nytimes/covid-19-data
"""

def time_to_dt(time):
    return dt.datetime.strptime(time, "%Y-%m-%d")

""" Preprocessing Products DataFrame"""

def preprocess_products_df(df: pd.DataFrame):
    df['PreK-12'] = df["Sector(s)"].apply(lambda x: True if (str(x)).find("PreK-12")!=-1 else False)
    df['HigherEd'] = df["Sector(s)"].apply(lambda x: True if (str(x)).find("Higher Ed")!=-1 else False)
    df['Corporate'] = df["Sector(s)"].apply(lambda x: True if (str(x)).find("Corporate")!=-1 else False)
    df = df.fillna("unknown")
    return df

""" Preprocess Districts DataFrame"""

def format_percent(val: str):
    if val is None or val=='unknown':
        return 'unknown'
    val = val[1:-1]
    val1 = str(float(val.split(', ')[0])*100)
    val2 = str(float(val.split(', ')[1])*100)
    return val1+'% - '+val2+'%'

def format_population(val: str):
    if val is None or val=='unknown':
        return 'unknown'
    val = val[1:-1]
    return val.split(', ')[0]+' - '+val.split(', ')[1]

def preprocess_districts_df(df: pd.DataFrame):
    df = df.fillna("unknown")
    df['pct_black/hispanic'] = df['pct_black/hispanic'].apply(format_percent)
    df['pct_free/reduced'] = df['pct_free/reduced'].apply(format_percent)
    df['county_connections_ratio'] = df['county_connections_ratio'].apply(format_percent)
    df['pp_total_raw'] = df['pp_total_raw'].apply(format_population)
    return df

""" Preprocess Engage DataFrames"""

def link_district_to_engage_df(loc_id: int, engage_files: list):
    for i in range(len(engage_files)):
        if(engage_files[i].find(str(loc_id)) != -1):
            return i
    return -1  

def preprocess_engage_dfs(engage_dfs: list, enage_files:list, districts_df: pd.DataFrame):
    for df in engage_dfs:
        df['dt'] = df['time'].apply(time_to_dt)
    districts_df['engage_file_id'] = districts_df['district_id'].apply(lambda x: link_district_to_engage_df(x, engage_files)) 

""" Preprocessing NY Times COVID cases DataFrame"""

def preprocess_nytime_cases_df(df: pd.DataFrame) :
    df['dt'] = df['date'].apply(time_to_dt)
    df = df[df.dt > dt.datetime(2020,1,1)]
    df = df[df.dt < dt.datetime(2020,12,31)]
    df = df.set_index('dt')
    return df  

""" Generate Maps That Connect Different Variables """

def generate_state_map(districts_df: pd.DataFrame, covid_case_df: pd.DataFrame, engage_dfs: list, engage_files: list):
    state_map = dict()
    for state in districts_df.state.value_counts().index:
        if(state!='unknown' and state!='District Of Columbia'):
            case_df = covid_case_df[covid_case_df.state == state]
            case_df['new_cases'] = case_df['cases'].transform(lambda s: s.sub(s.shift().fillna(0)).abs())

            ids = districts_df[districts_df.state == state].engage_file_id.values
            dfs = list()
            for i in ids:
                dfs.append(engage_dfs[i])
            engage_df = pd.concat(dfs)
            engage_df1 = engage_df.groupby(by=['dt'])[['pct_access', 'engagement_index']].mean()
            engage_df2 = engage_df.groupby(by=['dt', 'lp_id'])[['pct_access', 'engagement_index']].mean()
            engage_df2.reset_index().set_index('dt')

            state_map[state] = [case_df, engage_df1, engage_df2]
            
    return state_map

def generate_pct_black_hisp_map(districts_df: pd.DataFrame, engage_dfs: list):
    pct_black_hisp_map = dict()
    for val in np.unique(districts_df['pct_black/hispanic'].values):
        ids = districts_df[districts_df['pct_black/hispanic'] == val].engage_file_id.values
        dfs = list()
        for i in ids:
            dfs.append(engage_dfs[i])
        engage_df = pd.concat(dfs)
        engage_df1 = engage_df.groupby(by=['dt'])[['pct_access', 'engagement_index']].mean()
        engage_df2 = engage_df.groupby(by=['dt', 'lp_id'])[['pct_access', 'engagement_index']].mean()
        engage_df2.reset_index().set_index('dt')

        pct_black_hisp_map[val] = [engage_df1, engage_df2]
    return pct_black_hisp_map
        
def generate_pct_free_reduced_lunch_map(districts_df: pd.DataFrame, engage_dfs: list):
    pct_free_reduced_lunch_map = dict()
    for val in np.unique(districts_df['pct_free/reduced'].values):
        ids = districts_df[districts_df['pct_free/reduced'] == val].engage_file_id.values
        dfs = list()
        for i in ids:
            dfs.append(engage_dfs[i])
        engage_df = pd.concat(dfs)
        engage_df1 = engage_df.groupby(by=['dt'])[['pct_access', 'engagement_index']].mean()
        engage_df2 = engage_df.groupby(by=['dt', 'lp_id'])[['pct_access', 'engagement_index']].mean()
        engage_df2.reset_index().set_index('dt')

        pct_free_reduced_lunch_map[val] = [engage_df1, engage_df2]
    return pct_free_reduced_lunch_map

""" Generate Nation Wide DataFrames"""

def us_dfs(engage_dfs: list, covid_case_df: pd.DataFrame):
    engage_df_us = pd.concat(engage_dfs)
    engage_df_us = engage_df_us.groupby(by=['dt'])[['pct_access', 'engagement_index']].mean()
    
    covid_case_us = covid_case_df.groupby(by=['dt'])[['cases', 'deaths']].mean()
    covid_case_us['new_cases'] = covid_case_us['cases'].transform(lambda s: s.sub(s.shift().fillna(0)).abs())
    
    return engage_df_us, covid_case_us
