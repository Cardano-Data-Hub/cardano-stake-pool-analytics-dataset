"""
this is WIP and not intended for running in production
"""
import io
import os
import sys
import typer
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib import db_conn, boto3_resource #pylint-ignore: import-error

s3_resource = boto3_resource.get_resource('s3')
app = typer.Typer()

def generate_filepath(file_name, interval):
    """
    generates file path based on filename and schedule
    """

    if interval == "epoch":
        file_path = f"resources/core/{file_name}.sql"
    else:
        file_path = f"resources/core/{interval}/{file_name}.sql"
    return file_path

def generate_sql(file_path:str, pool_id:int = None):
    """
    generates SQL statement based on filepath
    """
    with open(file_path, 'r', encoding='utf-8') as file_dir:
        query = file_dir.read().strip('\n')
    # file_dir = open(file_path)
    # query =file_dir.read().strip('\n')
    if pool_id:
        query += f' WHERE pool_id = {pool_id}'
    copy_stmt = f"""COPY ({query}) TO STDIN \
            WITH (FORMAT csv, DELIMITER ',', QUOTE '"', HEADER TRUE)"""
    return copy_stmt

def load_to_s3(copy_stmt, s3_partition, bucket='stakepool-analytics'):
    """
    extracts data using the copy_stmt and loads to an s3 bucket
    """

    file_io = io.StringIO()
    conn = db_conn.init_conn()
    cur = conn.cursor()
    cur.copy_expert(copy_stmt, file_io)
    s3_resource.Object(bucket, f'{s3_partition}.csv').put(Body=file_io.getvalue())

@app.command()
def get_kpi(file_name, pool_id=None, interval='epoch'):
    FILE_PATH = generate_filepath(file_name, interval)
    S3_PARTITION = f"data/{file_name}"
    COPY_STMT = generate_sql(FILE_PATH, pool_id)
    load_to_s3(COPY_STMT, S3_PARTITION)

if __name__ == "__main__":

    app()