import pandas as pd
from datetime import datetime

from helpers.database import get_data_from_sql, save_df_to_db, run_query
from helpers.steam import get_steam_package_data
from helpers.logger import Logger
from helpers.utils import df_to_csv, get_packages
from transform.package_apps import transform_package_apps
from transform.package import transform_package


def package(df: pd.DataFrame):

    logger.info(f"package - starting")

    # make dataframe for raw data we want to save
    package_df = transform_package(df)
    logger.info(f"package - {len(package_df)} transformed rows")

    # save to raw
    save_df_to_db(df=package_df, name='package_raw', if_exists='replace')
    logger.info(f"package - saved to raw")
    
    # save to satage
    run_query('create_table_package_stage')
    rowcnt = run_query('raw_to_stage_package')
    logger.info(f"package - {rowcnt} modified/new rows saved to stage")

    # save to csv
    csv_df = get_data_from_sql('get_package')
    csv_file_path = df_to_csv(csv_df, name='package')
    logger.info(f"package - {len(csv_df)} saved to {csv_file_path}")
    logger.info(f"package - complete")


def package_apps(df: pd.DataFrame):

    logger.info(f"package_apps - starting")

    # make a dataframe with just the apps data
    package_apps_df = transform_package_apps(df)
    logger.info(f"package_apps - {len(package_apps_df)} transformed rows")

    # save to raw
    save_df_to_db(df=package_apps_df, name='package_apps_raw', if_exists='replace')
    logger.info(f"package_apps - saved to raw")

    # save to stage
    run_query('create_table_package_apps_stage')
    rowcnt = run_query('raw_to_stage_package_apps')
    logger.info(f"package_apps - {rowcnt} modified/new rows saved to stage")

    # save to csv
    csv_df = get_data_from_sql('get_package_apps')
    csv_file_path = df_to_csv(csv_df, name='package_apps')
    logger.info(f"package_apps - {len(csv_df)} saved to {csv_file_path}")
    logger.info(f"package_apps - complete")

def main():
    logger.info("starting")
    # read the packages to run
    packages = get_packages()

    # get the data
    logger.info("getting package data")
    data = get_steam_package_data(packages, refresh_data=False)      # set to false if just want to rerun data downloaded last time instead of making API calls
    logger.info(f"{len(data)} rows collected")

    # make dataframe with "_" normalization separator as that works better for running SQL on.
    df = pd.json_normalize(data, sep='_')
    # add current timestamp to the df
    df["load_ts"] = datetime.now()

    # run everything for package
    package(df)
    # run everything for package_apps
    package_apps(df)

    logger.info("complete")
    
if __name__ == '__main__':
    
    logger = Logger()
    main()
