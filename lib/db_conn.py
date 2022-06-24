import os
import psycopg2
from dotenv import load_dotenv


def init_conn():

    try:
        # Load env variables from the .env file
        load_dotenv()
        host = os.getenv("db_host")
        dbname = os.getenv("db_name")
        username = os.getenv("db_user")
        password = os.getenv("db_password")

        conn = _init_conn(host, dbname, username, password)

        return conn

    except Exception as e:
        print(e)


def _init_conn(host: str, dbname: str, username: str, password: str) -> str:

    conn = psycopg2.connect(host=host, dbname=dbname, user=username, password=password)

    return conn


if __name__ == "__main__":
    pass
