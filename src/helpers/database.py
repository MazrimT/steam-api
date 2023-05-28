from pathlib import Path
import sqlite3
from sqlite3 import Error
import pandas as pd



def get_query(file_name: str):
    """ reads a sql file and returns the content

    Arguments:
        file_name(str): name of the file to read

    Returns:
        str: the content of the sql file
    """
    sql_path = Path(__file__).parent.parent.joinpath('sql')

    with open(f"{sql_path}/{file_name}.sql", 'r') as f:
        query = f.read()
    
    return query


def get_con():
    """ returns a connection to the database

    Returns:
        sqlite3.connect()

    """
    db_file = Path(__file__).parent.parent.joinpath(f"data/database.db")
    return sqlite3.connect(db_file)

def save_df_to_db(df, name, if_exists):
    """ saves the content of a dataframe to database
    
    Arguments:
        df(pandas.DataFrame): the dataframe to save
        name(string): name of the table to save it to
        if_exists(string): "replace" or "append"
    """
    conn = get_con()

    df.to_sql(
        name=f"{name}",
        con=conn,
        if_exists=if_exists,
        index=False
    )
    conn.close()

def get_data_from_sql(file_name: str):
    """ reads data from the database using sql in a sql file

    Arguments:
        file_name(strwwwwwwwwwwwwwww): name of the file with the query to run
    
    Returns:
        pandas.DataFrame: dataframe of the result of the query
    """
    query = get_query(file_name)

    con = get_con()
    try:
        df = pd.read_sql(sql=query, con=con)
    except:
        df = pd.DataFrame()

    con.close()
   
    return df


def run_query(file_name: str):
    """ Runs a query towads database using sql in a sql file, only returns nr of rows touched, can not collect data to script

    Arguments:
        file_name(str): name of the file with the query to run
    
    Returns:
        int: number of rows modified by the script
        
    """
    queries = get_query(file_name).split(';')

    conn = get_con()
    curs = conn.cursor()
    rcnt = 0
    for query in queries:
        curs.execute(query)
        # not perfect if the query has too many parts but works for pure delete/update/inserts scripts
        if curs.rowcount > 0:
            rcnt += curs.rowcount

    conn.commit()
 
    curs.close()
    conn.close()

    return rcnt