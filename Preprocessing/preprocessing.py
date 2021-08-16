def time_to_dt(time):
    return dt.datetime.strptime(time, "%Y-%m-%d")

def link_district_to_engage_df(loc_id: int):
    for i in range(len(engage_files)):
        if(engage_files[i].find(str(loc_id)) != -1):
            return i
    return -1
