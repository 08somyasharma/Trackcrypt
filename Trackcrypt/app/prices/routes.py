from fastapi import APIRouter, Query
from app.db.dynamo import get_dynamodb

dynamodb = get_dynamodb()


router = APIRouter()


@router.get("/history")
def price_history(symbol: str = Query(...)):
    result = dynamodb.query(
        TableName="MarketPrices",
        IndexName="symbol-index",
        KeyConditionExpression="symbol = :s",
        ExpressionAttributeValues={
            ":s": {"S": symbol}
        },
        ScanIndexForward=True
    )

    return result.get("Items", [])
