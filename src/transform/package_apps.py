from helpers.utils import make_hash
import pandas as pd

def transform_package_apps(df: pd.DataFrame):

    columns = [
        "package_id", 
        "load_ts", 
        "apps"
    ]

    # add columns if missing for some reason, in order for things to not crash if we miss one
    for column in columns:
        if column not in df:
            df[column] = None

    # explode the apps array
    df = df.explode('apps')
    
    # remove all columns except package, timestamp and apps, and check that apps is not null/Nan
    df = df[["package_id", 'load_ts', 'apps']][df.apps.notnull()]

    # add app_id and name as columns
    df['app_id'] = df.apps.apply(lambda x: x['id'])
    df['name'] = df.apps.apply(lambda x: x['name'])

    # make a hash for incremental loads
    df['_hash'] = df[['name']].apply(make_hash, axis=1)
    # remove apps column
    df.pop('apps')

    return df
