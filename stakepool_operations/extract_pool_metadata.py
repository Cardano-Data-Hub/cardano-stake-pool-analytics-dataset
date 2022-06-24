# this is WIP and not intended for running in production

import os, sys
import requests
import pandas as pd
from dotenv import load_dotenv
from threading import Thread
from time import perf_counter
from psycopg2.extras import Json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib import db_conn

# to-do -> get ticker_url by querying pool_metadata_ref
# pool_meta_url = 'https://bluecheesestakehouse.com/bcsh.metadata.json'
def _extract_pool_metadata(cur, pool_id, url, data_raw):
    """
    """
    errored = 0
    error_reason = "website unreachable"
    try:
        print(f"extracting metadata for pool {pool_id}")
        pool_metadata = requests.get(url).json()
        extended_url = pool_metadata.get("extended")
        if extended_url is not None:
            pool_extended_metadata = requests.get(extended_url).json()
            extended_pool_data = [pool_id, extended_url, pool_extended_metadata, errored, error_reason]
            cur.execute("insert into pool_metadata_extended (pool_id, extended_url, extended_data) VALUES(%s,%s,%s)", (pool_id, extended_url, Json(pool_extended_metadata)))
            data_raw.append(extended_pool_data)
            print(f"inserting records for pool id {pool_id}")
        else:
            errored = 1
            error_reason = "extended url empty"
            cur.execute("insert into pool_metadata_extended (pool_id, errored, error_reason) VALUES(%s,%s, %s)", (pool_id, errored, error_reason))
            print(f"inserting records for pool id {pool_id}")
            extended_pool_data = [pool_id, '', '', errored, error_reason]
            data_raw.append(extended_pool_data)
    except Exception as e:
        errored = 1
        extended_pool_data = [pool_id, "", "", errored, error_reason]
        cur.execute("insert into pool_metadata_extended (pool_id, errored, error_reason) VALUES(%s,%s, %s)", (pool_id, errored, error_reason))
        print(f"inserting records for pool id {pool_id}")
        data_raw.append(extended_pool_data)

def extract_metadata_local():
    conn = db_conn.init_conn()
    cur = conn.cursor()
    cur.execute("select pool_id, url from analytics.v_recent_pool_metadata")
    pool_data = cur.fetchall()
    print("truncating the table")
    cur.execute("truncate table pool_metadata_extended")
    print("commiting truncate")
    conn.commit()

    data_raw = []

    threads = [Thread(target=_extract_pool_metadata, args=(cur, pool_id, url,data_raw))
            for pool_id, url in pool_data]
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    print("performing final commit")
    conn.commit()
    print("closing connection")
    conn.close()

    df = pd.DataFrame(data_raw, columns=['pool_id','extended_url','extended_data', 'errored', 'error_reason'])
    df.to_csv('data/metadata.csv', index=False)

if __name__ == "__main__":
    start_time = perf_counter()
    extract_metadata_local()
    end_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')
