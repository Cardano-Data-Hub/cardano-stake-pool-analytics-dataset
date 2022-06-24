import boto3, os
from dotenv import load_dotenv

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def get_resource(service:str):
    """
    Returns a boto3 resource for a specific service
    """
    resource = boto3.resource(service, 
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return resource