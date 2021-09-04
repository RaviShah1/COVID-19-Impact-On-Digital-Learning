""" 
The original data/input for all these functions can be located at the following sources:
1) https://www.kaggle.com/c/learnplatform-covid19-impact-on-digital-learning/data
2) https://github.com/nytimes/covid-19-data
"""

def time_to_dt(time):
    return dt.datetime.strptime(time, "%Y-%m-%d")

def preprocess_products_df(df: pd.DataFrame):
    df['PreK-12'] = df["Sector(s)"].apply(lambda x: True if (str(x)).find("PreK-12")!=-1 else False)
    df['HigherEd'] = df["Sector(s)"].apply(lambda x: True if (str(x)).find("Higher Ed")!=-1 else False)
    df['Corporate'] = df["Sector(s)"].apply(lambda x: True if (str(x)).find("Corporate")!=-1 else False)
    df = df.fillna("unknown")
    return df
    
def preprocess_districts_df(df: pd.DataFrame):
    df = df.fillna("unknown")
    return df
    
def link_district_to_engage_df(loc_id: int):
    for i in range(len(engage_files)):
        if(engage_files[i].find(str(loc_id)) != -1):
            return i
    return -1  

def preprocess_engage_dfs(engage_dfs: list):
    for df in engage_dfs:
        df['dt'] = df['time'].apply(time_to_dt)
    districts_df['engage_file_id'] = districts_df['district_id'].apply(lambda x: link_district_to_engage_df(engage_files)) 


def preprocess_nytime_cases_df(df: pd.DataFrame) :
    df['dt'] = df['date'].apply(time_to_dt)
    df = df[df.dt > dt.datetime(2020,1,1)]
    df = df[df.dt < dt.datetime(2020,12,31)]
    df = df.set_index('dt')
    return df  
    
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

def us_dfs(engage_dfs: list, covid_case_df: pd.DataFrame):
    engage_df_us = pd.concat(engage_dfs)
    engage_df_us = engage_df_us.groupby(by=['dt'])[['pct_access', 'engagement_index']].mean()
    
    covid_case_us = covid_case_df.groupby(by=['dt'])[['cases', 'deaths']].mean()
    covid_case_us['new_cases'] = covid_case_us['cases'].transform(lambda s: s.sub(s.shift().fillna(0)).abs())
    
    return engage_df_us, covid_case_us
