import uuid
from app.db.dynamo import get_dynamodb

dynamodb = get_dynamodb()


TABLE = "Watchlist"


def add_alert(user_id: str, data: dict):
    crypto_symbol = data.get("cryptoSymbol")
    alert_price = data.get("alertPrice")

    if not crypto_symbol or alert_price is None:
        return {"success": False, "error": "Invalid payload"}

    watchlist_id = str(uuid.uuid4())

    dynamodb.put_item(
        TableName=TABLE,
        Item={
            "watchListId": {"S": watchlist_id},
            "userId": {"S": user_id},
            "cryptoSymbol": {"S": crypto_symbol},
            "alertPrice": {"N": str(alert_price)},
        }
    )

    return {"success": True}


def list_alerts(user_id: str):
    result = dynamodb.query(
        TableName=TABLE,
        KeyConditionExpression="userId = :u",
        ExpressionAttributeValues={
            ":u": {"S": user_id}
        }
    )

    return result.get("Items", [])
