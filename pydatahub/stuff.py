import pandas as pd
import requests

import config

def get_entity(name, type):
    r = requests.get(config.url + '/entities', params={'name': name, 'type': type})
    return pd.Series(r.json()[0])

def get_entity_stats(entity, include_stats=None):
    if include_stats:
        r = requests.get(config.url + f"/entities/{entity['id']}/stats", params=include_stats)
    else:
        r = requests.get(config.url + f"/entities/{entity['id']}/stats")
    return pd.DataFrame(r.json())

def create_entity(e):
    return requests.post(config.url + '/entities', json=e)

def create_entity_stat(e, s):
    s['entityId'] = e['id']
    return requests.post(config.url + '/entity_stats', json=s)

def create_entity_stats(e, ss):
    e_id = e['id']
    for s in ss:
        s['entityId'] = e_id
    return requests.post(config.url + '/entity_stats_bulk', json=ss)

def join_entity_stats(e_s, s_df):
    s_df['entity_name'] = e_s['name']
    s_df['entity_type'] = e_s['type']
    return s_df

def get_data(entity_name, entity_type):
    e = get_entity(entity_name, entity_type)
    es = get_entity_stats(e)
    return join_entity_stats(e, es)

#def create_from_df(df, entity_column, start_time_col, end_time_col, stat_cols):
#    cols = [entity_column] + [start_time_col] + [end_time_col] + stat_cols
#    df_view = df[[cols]]
#    for entity in df.iterrows():
#        entity_name = entity[entity_column]
#        start_time = entity[start_time_col]
#        end_time = entity[end_time_col]
#        entity_stats = [entity[c] for c in stat_cols]
#        e = get_entity(entity_name)
#        request_bodies = [{
#            'startTime': start_time,
#            'endTime': end_time,
#            'name': entity_name,
#            'value': entity[c]
#        } for c in stat_cols]


print(get_data('Detroit', 'City'))
