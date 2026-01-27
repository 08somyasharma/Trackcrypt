import os
from dotenv import load_dotenv
import boto3

# Load .env
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# DynamoDB client
dynamodb = boto3.client(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# DynamoDB resource (recommended for table operations)
dynamo_resource = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Define tables
users_table = dynamo_resource.Table("Users")         # replace "Users" with your table name
watchlist_table = dynamo_resource.Table("Watchlist") # replace "Watchlist" with your table name
