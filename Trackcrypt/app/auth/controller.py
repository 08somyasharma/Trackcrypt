import uuid
from fastapi import HTTPException
from app.db.dynamo import get_dynamodb

dynamodb = get_dynamodb()

from app.auth.jwt import sign_token

USERS_TABLE = "Users"


def signup(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing email or password")

    user_id = str(uuid.uuid4())

    dynamodb.put_item(
        TableName=USERS_TABLE,
        Item={
            "userId": {"S": user_id},
            "email": {"S": email},
            "password": {"S": password},
        }
    )

    return {"token": sign_token({"userId": user_id})}


def signin(data: dict):
    user_id = data.get("userId")
    password = data.get("password")

    if not user_id or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    result = dynamodb.get_item(
        TableName=USERS_TABLE,
        Key={
            "userId": {"S": user_id}
        }
    )

    item = result.get("Item")

    if not item or item["password"]["S"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": sign_token({"userId": user_id})}
