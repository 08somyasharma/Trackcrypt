import uuid
import time
from app.db.dynamo import get_dynamodb

dynamodb = get_dynamodb()



def save_market_price(symbol, price):
    try:
        dynamodb.put_item(
            TableName="MarketPrices",
            Item={
                "priceId": str(uuid.uuid4()),
                "symbol": symbol,
                "timestamp": int(time.time() * 1000),
                "price": price,
            },
        )
    except Exception as e:
        # AWS keys nahi hain → ignore
        print("DynamoDB skipped (no credentials)")

