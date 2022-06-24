import pytest, os, sys, psycopg2
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib import db_conn, boto3_resource

db_user = 'fake_user'
db_password = 'fake_password'
db_host = 'fake_host'
db_name = 'fake_dbname'

def fake__init_conn(host, dbname, username, password):
    return f"<connection object at 0x000001C25C942D00; dsn: 'user={username} password=xxx dbname={dbname} host={host}', closed: 0>"
    pass

def test__init_conn(mocker):
    mocker.patch.object(db_conn,"_init_conn",fake__init_conn)
    assert db_conn._init_conn(db_host, db_name, db_user, db_password) == "<connection object at 0x000001C25C942D00; dsn: 'user=fake_user password=xxx dbname=fake_dbname host=fake_host', closed: 0>"

def fake_boto_resource(fake_service:str):
    return f"{fake_service} resource"

def test_mock_boto3_resource(mocker):
    mocker.patch.object(boto3_resource,"get_resource",fake_boto_resource)
    assert boto3_resource.get_resource("s3") == "s3 resource"
