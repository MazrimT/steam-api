import pandas as pd
from pathlib import Path
from hashlib import md5
import json

def df_to_csv(df: pd.DataFrame, name):
    """ saves a dataframe to csv in data folder

    Arguments:
        df: the dataframe to save
        name: name of the csv file

    Returns:
        str: file path to the saved file
    """

    output_path = Path(__file__).parent.parent.joinpath('data')
    file_path = f"{output_path}/{name}.csv"

    df.to_csv(file_path, index=False)

    return file_path

def make_hash(row):
    """ makes a hash of a dataframe row
    
    Arguments:
        row: a pandas dataframe row

    Returns:
        string: md5 hexdigest

        
    """

    # convert all values to str
    str_converted = [str(x) for x in row]

    # join to a single string
    temp = "|".join(str_converted).encode('utf-8')

    # make md5 hash in hex format
    hash = md5(temp).hexdigest()
    
    return hash


def get_packages():
    """ reads the input_packages.json file

    Returns:
        list: list of unique package ids
    
    """
    
    data_path = Path(__file__).parent.parent.joinpath('data')    

    with open(f"{data_path}/input_packages.json", 'r') as f:
        packages = json.load(f)

    return list(set(packages))