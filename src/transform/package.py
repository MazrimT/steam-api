from helpers.utils import make_hash
import pandas as pd

def transform_package(df: pd.DataFrame):

    columns = [
        "package_id", 
        "load_ts", 
        "name", 
        "price_currency", 
        "price_initial", 
        "price_final", 
        "price_discount_percent", 
        "price_individual",
        "platforms_windows",
        "platforms_mac",
        "platforms_linux",
        "release_date_coming_soon",
        "release_date_date"
    ]

    # pandas doesn't seem to like big changes being made on the same DF so we make a copy
    df2 = df.copy()
    
    # add columns if missing for some reason, in order for things to not crash if we miss one
    for column in columns:
        if column not in df2:
            df2[column] = None


    # only pick columns we want to keep
    df2 = df2[columns]

    # make a hash for incremental loads
    df2['_hash'] = df2[
        [
            "price_currency", 
            "price_initial", 
            "price_final", 
            "price_discount_percent", 
            "price_individual",
            "platforms_windows",
            "platforms_mac",
            "platforms_linux",
            "release_date_coming_soon",
            "release_date_date"
        ]
    ].apply(make_hash, axis=1)

    return df2